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
import datetime
import os

import flask_jwt_extended as fjwt
import PyMatcha.models.user as user
from flask import Blueprint
from flask import request
from PyMatcha.errors import BadRequestError
from PyMatcha.errors import NotFoundError
from PyMatcha.errors import UnauthorizedError
from PyMatcha.models.tag import Tag
from PyMatcha.success import Success
from PyMatcha.utils import hash_password
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.mail import send_mail_text

User = user.User
get_user = user.get_user

profile_bp = Blueprint("profile", __name__)

REQUIRED_PARAMS_COMPLETE_PROFILE = {"gender": str, "birthdate": int, "orientation": str, "bio": str, "tags": list}
REQUIRED_PARAMS_EDIT_PROFILE = {
    "first_name": str,
    "last_name": str,
    "username": str,
    "bio": str,
    "gender": str,
    "orientation": str,
    "birthdate": int,
    "tags": list,
}


@profile_bp.route("/profile/complete", methods=["POST"])
@fjwt.jwt_required
@validate_params(REQUIRED_PARAMS_COMPLETE_PROFILE)
def complete_profile():
    current_user = fjwt.current_user
    if current_user.is_profile_completed:
        raise BadRequestError(
            "The user has already completed his profile", "Go to your profile settings to edit your profile"
        )
    data = request.get_json()
    orientation = data["orientation"]
    bio = data["bio"]
    tags = data["tags"]
    gender = data["gender"]
    birthdate = data["birthdate"]

    for tag in tags:
        Tag.create(name=tag, user_id=current_user.id)

    current_user.orientation = orientation
    current_user.bio = bio
    current_user.is_profile_completed = True
    current_user.gender = gender
    current_user.birthdate = datetime.date.fromtimestamp(int(birthdate))
    current_user.save()
    return Success("Profile completed !")


@profile_bp.route("/profile/edit", methods=["PUT"])
@fjwt.jwt_required
@validate_params(REQUIRED_PARAMS_EDIT_PROFILE)
def edit_profile():
    current_user = fjwt.current_user
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile", "Complete your profile and try again")
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    username = data["username"]
    bio = data["bio"]
    gender = data["gender"]
    orientation = data["orientation"]
    birthdate = data["birthdate"]

    try:
        get_user(username)
    except NotFoundError:
        pass
    else:
        raise BadRequestError("Username taken", "Try again")

    if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
        raise BadRequestError("Orientation must be heterosexual, homosexual, bisexual or other", "Try again")

    if gender not in ["male", "female", "other"]:
        raise BadRequestError("Gender must be male, female or other", "Try again")

    birthdate = datetime.date.fromtimestamp(birthdate)

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.username = username
    current_user.bio = bio
    current_user.gender = gender
    current_user.orientation = orientation
    current_user.birthdate = birthdate
    current_user.save()
    return Success("User successfully modified !")


@profile_bp.route("/profile/edit/email", methods=["PUT"])
@fjwt.jwt_required
@validate_params({"email": str})
def edit_email():
    data = request.get_json()
    new_email = data["email"].lower()
    current_user = fjwt.current_user
    if current_user.email == new_email:
        raise BadRequestError("The new email is the same as the old one !", "Try again")
    current_user.email = new_email
    current_user.is_confirmed = False
    current_user.save()
    token = generate_confirmation_token(email=new_email, token_type="confirm")
    send_mail_text.delay(
        dest=data["email"],
        subject="Confirm your new email for PyMatcha",
        body=os.getenv("APP_URL") + "/auth/confirm/" + token,
    )
    return Success("Email sent for new email")


@profile_bp.route("/profile/edit/password", methods=["PUT"])
@fjwt.jwt_required
@validate_params({"old_password": str, "new_password": str})
def edit_password():
    data = request.get_json()
    old_password = data["old_password"]
    new_password = data["new_password"]
    current_user = fjwt.current_user
    if not current_user.check_password(old_password):
        raise UnauthorizedError("Incorrect password", "Try again")
    current_user.password = hash_password(new_password)
    current_user.save()
    # TODO: Send mail
    send_mail_text.delay(
        dest=current_user.email,
        subject="Password change notification",
        body=f"Your password was changed at {datetime.datetime.utcnow()}."
        f" If you believe it wasn't you, please change it immediatly",
    )
    return Success("User password successfully updated.")
