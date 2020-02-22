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

import os
import datetime

from flask import Blueprint, request, redirect

from werkzeug.exceptions import BadRequest

from itsdangerous import SignatureExpired, BadSignature


from PyMatcha.models import User, get_user
from PyMatcha.errors import BadRequestError, ConflictError, NotFoundError
from PyMatcha.success import SuccessOutputMessage
from PyMatcha.utils.confirm_token import generate_confirmation_token, confirm_token
from PyMatcha.utils.mail import send_mail_text

REQUIRED_KEYS_USER_CREATION = ["username", "email", "password"]


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def api_create_user():
    # If the json body is missing something (`,` for example), throw an error
    try:
        data = request.get_json()
    except BadRequest:
        raise BadRequestError("The Json Body is malformed", "Please check it and try again")

    # If the data dict is empty
    if not data:
        raise BadRequestError("Missing json body.", "Please fill your json body")

    missing = []
    for item in REQUIRED_KEYS_USER_CREATION:
        # If a key is missing in the sent data
        if item not in data.keys():
            missing.append(item)
    if missing:
        raise BadRequestError(
            "Missing keys {} to create user.".format(missing), "Complete your json body and try again"
        )

    for item in data.keys():
        # If there's an unwanted key in the sent data
        if item not in REQUIRED_KEYS_USER_CREATION:
            raise BadRequestError(
                "You can't specify key '{}'.".format(item),
                "You are only allowed to specify the fields {} " "when creating a user.".format(request),
            )

    for key, value in data.items():
        if value is None or value == "":
            raise BadRequestError(f"The item {key} cannot be None or empty", "Please try again.")

    data["email"] = data["email"].lower()

    try:
        new_user = User.register(email=data["email"], username=data["username"], password=data["password"])
    except ConflictError as e:
        raise e
    else:
        token = generate_confirmation_token(email=data["email"])
        send_mail_text(
            dest=data["email"],
            subject="Confirm your email for PyMatcha",
            body=os.getenv("APP_URL") + "/auth/confirm/" + token,
        )
        return SuccessOutputMessage("email", new_user.email, "New user successfully created.")


@auth_bp.route("/auth/confirm/<token>", methods=["GET"])
def confirm_email(token):
    try:
        email = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            return redirect("/?success=false?message=Signature expired")
        else:
            return redirect("/?success=false?message=Bad Signature")
    else:
        try:
            user = get_user(email)
        except NotFoundError:
            return redirect("/?success=false?message=User not found")
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.utcnow()
        user.save()
        return redirect("/?success=true&message=User confirmed")
