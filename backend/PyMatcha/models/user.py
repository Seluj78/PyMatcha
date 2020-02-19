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

import hashlib

from datetime import datetime

from PyMatcha.utils import hash_password
from PyMatcha.utils.orm import Model, Field

import Geohash


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
    birthdate = Field(datetime)
    geohash = Field(str)
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
            raise Exception("User not in database")

    @staticmethod
    def create(
        first_name,
        last_name,
        email,
        username,
        password,
        bio,
        gender,
        birthdate,
        geohash,
        heat_score=0,
        online=False,
        date_joined=datetime.utcnow(),
        date_lastseen=datetime.utcnow(),
        deleted=False,
    ):
        # Check email availability
        if User.get(email=email):
            raise ValueError("Email {} taken".format(email))

        # Check username availability
        if User.get(username=username):
            raise ValueError("Username {} taken".format(username))

        # Check correct gender
        if gender not in ["male", "female", "other"]:
            raise ValueError("Gender must be male, female or other, not {}".format(gender))

        # Check correct geohash
        try:
            Geohash.decode(geohash)
        except ValueError as e:
            raise e

        # Encrypt password
        password = hash_password(password)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            bio=bio,
            gender=gender,
            birthdate=birthdate,
            geohash=geohash,
            heat_score=heat_score,
            online=online,
            date_joined=date_joined,
            date_lastseen=date_lastseen,
            deleted=deleted,
        )
        new_user.save()
        return new_user

    # def essential(self):
    #     return {
    #         "id": self.id,
    #         "fname": self.fname,
    #         "lname": self.lname
    #     }
