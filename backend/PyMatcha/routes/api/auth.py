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

from itsdangerous import SignatureExpired, BadSignature


from PyMatcha.models import User, get_user
from PyMatcha.errors import ConflictError, NotFoundError, BadRequestError
from PyMatcha.success import SuccessOutputMessage, Success
from PyMatcha.utils.confirm_token import generate_confirmation_token, confirm_token
from PyMatcha.utils.mail import send_mail_text
from PyMatcha.utils.decorators import validate_required_params
from PyMatcha.utils import hash_password

REQUIRED_KEYS_USER_CREATION = ["username", "email", "password"]
REQUIRED_KEYS_PASSWORD_FORGOT = ["email"]
REQUIRED_KEYS_PASSWORD_RESET = ["token", "password"]

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
@validate_required_params(REQUIRED_KEYS_USER_CREATION)
def api_create_user():
    data = request.get_json()
    data["email"] = data["email"].lower()

    try:
        new_user = User.register(email=data["email"], username=data["username"], password=data["password"])
    except ConflictError as e:
        raise e
    else:
        token = generate_confirmation_token(email=data["email"], token_type="confirm")
        send_mail_text(
            dest=data["email"],
            subject="Confirm your email for PyMatcha",
            body=os.getenv("APP_URL") + "/auth/confirm/" + token,
        )
        return SuccessOutputMessage("email", new_user.email, "New user successfully created.")


@auth_bp.route("/auth/confirm/<token>", methods=["GET"])
def confirm_email(token):
    try:
        email, token_type = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            return redirect("/?type=confirm&success=false?message=Signature expired")
        else:
            return redirect("/?type=confirm&success=false?message=Bad Signature")
    else:
        if token_type != "confirm":
            return redirect("/?type=confirm&success=false?message=Wrong token type")
        try:
            user = get_user(email)
        except NotFoundError:
            return redirect("/?type=confirm&success=false?message=User not found")
        if user.is_confirmed:
            return redirect("/?type=confirm&success=false?message=User already confirmed")
        user.is_confirmed = True
        user.confirmed_on = datetime.datetime.utcnow()
        user.save()
        return redirect("/?type=confirm&success=true&message=User confirmed")


@auth_bp.route("/auth/password/forgot", methods=["POST"])
@validate_required_params(REQUIRED_KEYS_PASSWORD_FORGOT)
def forgot_password():
    data = request.get_json()
    try:
        get_user(data["email"])
    except NotFoundError:
        pass
    else:
        token = generate_confirmation_token(email=data["email"], token_type="reset")
        send_mail_text(
            dest=data["email"],
            subject="Password reset for PyMatcha",
            body=os.getenv("APP_URL") + "/reset_password?token=" + token,
        )
    return Success("Password reset mail sent successfully if user exists in DB")


@auth_bp.route("/auth/password/reset", methods=["POST"])
@validate_required_params(REQUIRED_KEYS_PASSWORD_RESET)
def reset_password():
    data = request.get_json()
    try:
        email, token_type = confirm_token(data["token"], expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            raise BadRequestError("Signature Expired.", "Request another password reset and try again.")
        else:
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        if token_type != "reset":
            raise BadRequestError("Wrong token type", "Try again with the correct type")
        try:
            user = get_user(email)
        except NotFoundError:
            raise NotFoundError("User not found", "Try again with another user.")
        if user.previous_reset_token == data["token"]:
            raise BadRequestError("Token already used", "Please request a new one")
        user.password = hash_password(data["password"])
        user.previous_reset_token = data["token"]
        user.save()
        return Success("Password reset successful")
