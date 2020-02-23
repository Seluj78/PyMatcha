"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/gmorer
    <jlasne@student.42.fr> - <gmorer@student.42.fr>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

import json
import hashlib

from typing import Dict, List, Optional, Any

from datetime import datetime

from PyMatcha.utils import hash_password
from PyMatcha.utils.orm import Model, Field
from PyMatcha.utils import create_user_table

from PyMatcha.errors import ConflictError, NotFoundError

import PyMatcha.models.user_image as user_image

import Geohash

UserImage = user_image.UserImage


class User(Model):
    table_name = "users"

    id = Field(int, modifiable=False)
    first_name = Field(str)
    last_name = Field(str)
    email = Field(str)
    username = Field(str)
    password = Field(str, hidden=True)
    bio = Field(str)
    gender = Field(str)
    orientation = Field(str)
    birthdate = Field(datetime)
    geohash = Field(str)
    tags = Field(dict)
    heat_score = Field(int)
    is_online = Field(bool)
    date_joined = Field(datetime)
    date_lastseen = Field(datetime)
    is_profile_completed = Field(bool)
    is_confirmed = Field(bool)
    confirmed_on = Field(datetime)
    previous_reset_token = Field(str)

    def before_init(self, data):
        pass
        # Not used, use User.create and password will be hashed.
        # if "password" in data:
        #     self.password.value = hash_password(data["password"])

    def check_password(self, password: str) -> bool:
        _hash, salt = self.password.split(":")
        return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def delete(self):
        if self.id:
            with self.db.cursor() as c:
                c.execute(
                    """
                UPDATE {0} SET deleted = 1 
                WHERE id=CAST({1} AS INT)
                """.format(
                        self.table_name, self.id
                    )
                )
                self.db.commit()
        else:
            raise NotFoundError("User not in database", "Try again")

    @staticmethod
    def create(
        first_name: str,
        last_name: str,
        email: str,
        username: str,
        password: str,
        bio: str,
        gender: str,
        orientation: str,
        birthdate: datetime,
        geohash: str,
        tags,
        heat_score: int = 0,
        is_online: bool = False,
        date_joined: datetime = datetime.utcnow(),
        date_lastseen: datetime = datetime.utcnow(),
        is_profile_completed: bool = False,
        is_confirmed: bool = False,
        confirmed_on: datetime = None,
    ) -> User:
        # Check email availability
        if User.get(email=email):
            raise ConflictError("Email {} taken".format(email), "Use another email")

        # Check username availability
        if User.get(username=username):
            raise ConflictError("Username {} taken".format(username), "Try another username")

        # Check correct gender
        if gender not in ["male", "female", "other"]:
            raise ConflictError("Gender must be male, female or other, not {}".format(gender), "Try again")

        # Check correct orientation
        if orientation not in ["heterosexual", "homosexual", "bisexual"]:
            raise ConflictError(
                "Sexual Orientation must be heterosexual, homosexual or bisexual, not {}".format(orientation),
                "Try again",
            )

        # Check correct geohash
        try:
            Geohash.decode(geohash)
        except ValueError as e:
            raise e

        # TODO: Check if all tags are set in tags

        # Encrypt password
        password = hash_password(password)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            username=username,
            password=password,
            bio=bio,
            gender=gender,
            orientation=orientation,
            birthdate=birthdate,
            geohash=geohash,
            tags=str(json.dumps(tags)),
            heat_score=heat_score,
            is_online=is_online,
            date_joined=date_joined,
            date_lastseen=date_lastseen,
            is_profile_completed=is_profile_completed,
            is_confirmed=is_confirmed,
            confirmed_on=confirmed_on,
            previous_reset_token=None,
        )
        new_user.save()
        return new_user

    @staticmethod
    def register(email: str, username: str, password: str) -> User:
        # Check email availability
        try:
            User.get(email=email)
        except ValueError:
            pass
        else:
            raise ConflictError("Email {} taken".format(email), "Use another email")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            raise ConflictError("Username {} taken".format(username), "Try another username")

        # Encrypt password
        password = hash_password(password)

        new_user = User(
            email=email.lower(),
            username=username,
            password=password,
            first_name="",
            last_name="",
            bio="",
            gender="other",
            orientation="bisexual",
            birthdate=datetime.utcnow(),
            geohash="",
            tags="",
            heat_score=0,
            is_online=False,
            date_joined=datetime.utcnow(),
            date_lastseen=datetime.utcnow(),
            is_profile_completed=False,
            is_confirmed=False,
            confirmed_on=None,
            previous_reset_token=None,
        )
        new_user.save()
        return new_user

    def get_all_info(self) -> Dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "bio": self.bio,
            "gender": self.gender,
            "orientation": self.orientation,
            "birthdate": self.birthdate,
            "geohash": self.geohash,
            "tags": json.loads(self.tags),
            "heat_score": self.heat_score,
            "is_online": self.online,
            "date_joined": self.date_joined,
            "date_lastseen": self.date_lastseen,
            "is_profile_completed": self.profile_completed,
            "is_confirmed": self.is_confirmed,
            "confirmed_on": self.confirmed_on,
            "previous_reset_token": self.previous_reset_token,
        }

    @classmethod
    def create_table(cls):
        create_user_table(cls.db)

    def get_images(self) -> List[UserImage]:
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT user_images.id as id, user_images.user_id as user_id, user_images.description as description, 
                user_images.timestamp as timestamp, user_images.is_primary as is_primary
                FROM users 
                INNER JOIN user_images on users.id = user_images.user_id 
                WHERE users.id = CAST({} AS INT)
                """.format(
                    self.id
                )
            )
            images = c.fetchall()
            image_list = []
            for image in images:
                image_list.append(UserImage(image))
        return image_list

    def get_base_info(self):
        return {
            "email": self.email,
            "username": self.username,
            "is_online": self.is_online,
            "date_lastseen": self.date_lastseen,
        }


def get_user(uid: Any[int, str]) -> Optional[User]:

    not_found = 0
    # These initializations are to make PEP happy and silence warnings
    f_user = None

    if isinstance(uid, str):
        uid = uid.lower()

    try:
        user = User.get(id=uid)
    except ValueError:
        not_found += 1
    else:
        f_user = user
    try:
        user = User.get(username=uid)
    except ValueError:
        not_found += 1
    else:
        f_user = user
    try:
        user = User.get(email=uid)
    except ValueError:
        not_found += 1
    else:
        f_user = user
    # If none of those worked, throw an error
    if not_found == 3:
        raise NotFoundError("User {} not found.".format(uid), "Try again with another uid")
    return f_user
