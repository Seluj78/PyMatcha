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

import datetime
import hashlib
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import Geohash
import PyMatcha.models.user_image as user_image
from PyMatcha.errors import ConflictError
from PyMatcha.errors import NotFoundError
from PyMatcha.models.tag import Tag
from PyMatcha.utils import create_user_table
from PyMatcha.utils import hash_password
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model

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
    birthdate = Field(datetime.date)
    geohash = Field(str)
    heat_score = Field(int)
    is_online = Field(bool)
    date_joined = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    date_lastseen = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    is_profile_completed = Field(bool)
    is_confirmed = Field(bool)
    confirmed_on = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    previous_reset_token = Field(str)

    def before_init(self, data):
        pass
        # Not used, use User.create and password will be hashed.
        # if "password" in data:
        #     self.password.value = hash_password(data["password"])

    def check_password(self, password: str) -> bool:
        logging.debug("Checking password again {} hashed password".format(self.id))
        _hash, salt = self.password.split(":")
        return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

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
        birthdate: datetime.date,
        geohash: str,
        heat_score: int = 0,
        is_online: bool = False,
        date_joined: datetime.datetime = datetime.datetime.utcnow(),
        date_lastseen: datetime.datetime = datetime.datetime.utcnow(),
        is_profile_completed: bool = False,
        is_confirmed: bool = False,
        confirmed_on: datetime.datetime = None,
    ) -> User:
        # Check email availability
        try:
            User.get(email=email)
        except ValueError:
            pass
        else:
            logging.error("Email {} taken".format(email))
            raise ConflictError("Email {} taken".format(email), "Use another email")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            logging.error("Username {} taken".format(username))
            raise ConflictError("Username {} taken".format(username), "Try another username")

        # Check correct gender
        if gender not in ["male", "female", "other"]:
            logging.error("Gender must be male, female or other, not {}".format(gender))
            raise ConflictError("Gender must be male, female or other, not {}".format(gender), "Try again")

        # Check correct orientation
        if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
            logging.error(
                "Sexual Orientation must be heterosexual, homosexual, bisexual or other, not {}".format(orientation)
            )
            raise ConflictError(
                "Sexual Orientation must be heterosexual, homosexual, bisexual or other, not {}".format(orientation),
                "Try again",
            )

        # Check correct geohash
        try:
            Geohash.decode(geohash)
        except ValueError as e:
            logging.error("Geohash error: {}".format(e))
            raise e

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
        logging.debug("New user {} created".format(new_user.email))
        return new_user

    @staticmethod
    def register(email: str, username: str, password: str, first_name: str, last_name: str) -> User:
        # Check email availability
        try:
            User.get(email=email)
        except ValueError:
            pass
        else:
            logging.error("Email {} taken".format(email))
            raise ConflictError("Email {} taken".format(email), "Use another email")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            logging.error("Username {} taken".format(username))
            raise ConflictError("Username {} taken".format(username), "Try another username")

        # Encrypt password
        password = hash_password(password)

        new_user = User(
            email=email.lower(),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio="",
            gender="other",
            orientation="bisexual",
            birthdate=None,
            geohash=None,
            heat_score=0,
            is_online=False,
            date_joined=datetime.datetime.utcnow(),
            date_lastseen=datetime.datetime.utcnow(),
            is_profile_completed=False,
            is_confirmed=False,
            confirmed_on=None,
            previous_reset_token=None,
        )
        new_user.save()
        logging.debug("New user {} created".format(new_user.email))
        return new_user

    def get_all_info(self) -> Dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "username": self.username,
            "bio": self.bio,
            "gender": self.gender,
            "orientation": self.orientation,
            "birthdate": self.birthdate,
            "geohash": self.geohash,
            "tags": [t.name for t in self.get_tags()],
            "heat_score": self.heat_score,
            "is_online": self.is_online,
            "date_joined": self.date_joined,
            "date_lastseen": self.date_lastseen,
            "is_profile_completed": self.is_profile_completed,
            "is_confirmed": self.is_confirmed,
            "confirmed_on": self.confirmed_on,
        }

    @classmethod
    def create_table(cls):
        create_user_table(cls.db)

    def get_images(self) -> List[UserImage]:
        logging.debug("Getting all images for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT user_images.id as id, user_images.user_id as user_id, user_images.description as description, 
                user_images.timestamp as timestamp, user_images.is_primary as is_primary
                FROM users 
                INNER JOIN user_images on users.id = user_images.user_id 
                WHERE users.id = CAST({} AS UNSIGNED)
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
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_online": self.is_online,
            "date_lastseen": self.date_lastseen,
        }

    def get_tags(self):
        logging.debug("Getting all tags for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT tags.id as id, tags.user_id as user_id, tags.name as name
                FROM users 
                INNER JOIN tags on users.id = tags.user_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            tags = c.fetchall()
            tags_list = []
            for t in tags:
                tags_list.append(Tag(t))
        return tags_list


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
        logging.error("User {} not found.".format(uid))
        raise NotFoundError("User {} not found.".format(uid), "Try again with another uid")
    logging.debug("Found user {} from {}".format(f_user.id, uid))
    return f_user
