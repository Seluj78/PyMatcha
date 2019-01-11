# coding=utf-8

"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/ynacache
    <jlasne@student.42.fr> - <ynacache@student.42.fr>

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

import uuid
import datetime

from peewee import CharField, DateTimeField, TextField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash

from flask_admin.contrib.peewee import ModelView
from flask_login import UserMixin
from PyMatcha import login

from PyMatcha.models import BaseModel

class User(UserMixin, BaseModel):
    """
    This is the user model used in the DB
    """

    client_id = CharField(
        default=str(uuid.uuid4()), help_text="The user's unique identifier", verbose_name="Unique Identifier"
    )
    first_name = CharField(help_text="The user's first name", verbose_name="First Name")
    last_name = CharField(help_text="The user's last name", verbose_name="Last Name")
    email = CharField(help_text="The user's email address", verbose_name="Email Address")
    username = CharField(max_length=80, help_text="User's Username", verbose_name="Username")
    password = CharField(max_length=80, help_text="User's Password", verbose_name="Password")

    profile_picture_url = CharField(
        default="https://moonvillageassociation.org/wp-content/uploads/2018/06/default-profile-picture1-744x744.jpg",
        help_text="The user's profile picture image link",
        verbose_name="PP Image URL",
    )
    description = TextField(null=True, help_text="The user's description", verbose_name="User's Description")
    dt_registered = DateTimeField(
        default=datetime.datetime.utcnow(),
        help_text="When the user registered to PyMatcha",
        verbose_name="Date and Time Registered",
    )
    dt_last_login = DateTimeField(
        default=datetime.datetime.utcnow(),
        help_text="When the user last logged in to PyMatcha",
        verbose_name="Date and Time Last Logged in",
    )

    is_confirmed = BooleanField(
        default=False, help_text="Has the user confirmed his email", verbose_name="Is Confirmed"
    )
    dt_confirmed = DateTimeField(
        null=True, help_text="When the user confirmed his email adress", verbose_name="Date and Time Confirmed"
    )
    confirmed_by = CharField(null=True, help_text="Who confirmed the user", verbose_name="Confirmed By")

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(client_id):
    return User.query.get(client_id)

class UserAdmin(ModelView):
    pass