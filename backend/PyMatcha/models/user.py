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

import json
import hashlib

from datetime import datetime

from PyMatcha.utils import hash_password
from PyMatcha.utils.orm import Model, Field
from PyMatcha.utils import create_user_table, create_user_images_table

from PyMatcha.errors import ConflictError, NotFoundError

import Geohash


class UserImage(Model):
    table_name = "user_images"

    id = Field(int, modifiable=False)
    user_id = Field(int)
    image_path = Field(str)

    def before_init(self, data):
        pass

    def delete(self):
        if self.id:
            with self.db.cursor() as c:
                c.execute(
                    """
                UPDATE {0} SET deleted = 1 
                WHERE id='{1}'
                """.format(
                        self.table_name, self.id
                    )
                )
                self.db.commit()
        else:
            raise NotFoundError("Image not in database", "Try again")

    @staticmethod
    def create(user_id, image_path):
        new_image = UserImage(user_id=user_id, image_path=image_path)
        new_image.save()
        return new_image

    def get_all_info(self):
        return {"id": self.id, "user_id": self.user_id, "image_path": self.image_path}

    @classmethod
    def create_table(cls):
        create_user_images_table(cls.db)


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
    online = Field(bool)
    date_joined = Field(datetime)
    date_lastseen = Field(datetime)
    deleted = Field(bool, modifiable=False, hidden=True)

    def before_init(self, data):
        pass
        # Not used, use User.create and password will be hashed.
        # if "password" in data:
        #     self.password.value = hash_password(data["password"])

    def check_password(self, password):
        _hash, salt = self.password.split(":")
        return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def delete(self):
        if self.id:
            with self.db.cursor() as c:
                c.execute(
                    """
                UPDATE {0} SET deleted = 1 
                WHERE id='{1}'
                """.format(
                        self.table_name, self.id
                    )
                )
                self.db.commit()
        else:
            raise NotFoundError("User not in database", "Try again")

    @staticmethod
    def create(
        first_name,
        last_name,
        email,
        username,
        password,
        bio,
        gender,
        orientation,
        birthdate,
        geohash,
        tags,
        heat_score=0,
        online=False,
        date_joined=datetime.utcnow(),
        date_lastseen=datetime.utcnow(),
        deleted=False,
    ):
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
            online=online,
            date_joined=date_joined,
            date_lastseen=date_lastseen,
            deleted=deleted,
        )
        new_user.save()
        return new_user

    def get_all_info(self):
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
            "online": self.online,
            "date_joined": self.date_joined,
            "date_lastseen": self.date_lastseen,
            "deleted": self.deleted,
        }

    @classmethod
    def create_table(cls):
        create_user_table(cls.db)

    def get_images(self):
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT user_images.id as id, user_images.user_id as user_id, user_images.image_path as image_path 
                FROM users 
                INNER JOIN user_images on users.id = user_images.user_id 
                WHERE user_id = {}
                """.format(
                    self.id
                )
            )
            images = c.fetchall()
            image_list = []
            for image in images:
                image_list.append(UserImage(image))
        return image_list


def get_user(uid):

    not_found = 0
    # These initializations are to make PEP happy and silence warnings
    f_user = None

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
