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

from flask import Blueprint, request, redirect, current_app

from itsdangerous import SignatureExpired, BadSignature

import flask_jwt_extended as fjwt

from PyMatcha import redis

import PyMatcha.models.user as user
from PyMatcha.errors import ConflictError, NotFoundError, BadRequestError, UnauthorizedError
from PyMatcha.success import SuccessOutputMessage, Success, SuccessOutput
from PyMatcha.utils.confirm_token import generate_confirmation_token, confirm_token
from PyMatcha.utils.mail import send_mail_text
from PyMatcha.utils.decorators import validate_required_params
from PyMatcha.utils import hash_password


User = user.User
get_user = user.get_user

REQUIRED_KEYS_USER_CREATION = {"username": str, "email": str, "password": str}
REQUIRED_KEYS_PASSWORD_FORGOT = {"email": str}
REQUIRED_KEYS_PASSWORD_RESET = {"token": str, "password": str}
REQUIRED_KEYS_LOGIN = {"username": str, "password": str}
REQUIRED_KEYS_NEW_EMAIL_CONF = {"email": str}

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
        send_mail_text.delay(
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
            return redirect("/?type=confirm&success=false&message=Signature expired")
        else:
            return redirect("/?type=confirm&success=false&message=Bad Signature")
    else:
        if token_type != "confirm":
            return redirect("/?type=confirm&success=false&message=Wrong token type")
        try:
            u = get_user(email)
        except NotFoundError:
            return redirect("/?type=confirm&success=false&message=User not found")
        if u.is_confirmed:
            return redirect("/?type=confirm&success=false&message=User already confirmed")
        u.is_confirmed = True
        u.confirmed_on = datetime.datetime.utcnow()
        u.save()
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
        send_mail_text.delay(
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
            u = get_user(email)
        except NotFoundError:
            raise NotFoundError("User not found", "Try again with another user.")
        if u.previous_reset_token == data["token"]:
            raise BadRequestError("Token already used", "Please request a new one")
        u.password = hash_password(data["password"])
        u.previous_reset_token = data["token"]
        u.save()
        return Success("Password reset successful")


@auth_bp.route("/auth/login", methods=["POST"])
@validate_required_params(REQUIRED_KEYS_LOGIN)
def auth_login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    try:
        u = get_user(username)
    except NotFoundError:
        raise NotFoundError("User not found", "Try again with a different username")
    if not u.check_password(password):
        raise UnauthorizedError("Incorrect Password", "Try again")

    # access_token = fjwt.create_access_token(
    #     identity=get_user_safe_dict(user), expires_delta=datetime.timedelta(hours=2)
    # )
    # TODO: Handle expiry for token
    if not u.is_confirmed:
        raise UnauthorizedError("User needs to be confirmed first.", "Try again when you have confirmed your email")
    u.is_online = True
    u.date_lastseen = datetime.datetime.utcnow()
    u.save()
    access_token = fjwt.create_access_token(identity=u.get_base_info(), fresh=True)
    redis.set("user:" + u.id, u.date_lastseen.timestamp())
    return SuccessOutput("access_token", access_token)


@auth_bp.route("/auth/confirm/new", methods=["POST"])
@validate_required_params(REQUIRED_KEYS_NEW_EMAIL_CONF)
def request_new_email_conf():
    current_app.logger.debug("/auth/confirm/new -> Call")
    data = request.get_json()
    email = data["email"]
    try:
        u = get_user(email)
    except NotFoundError:
        current_app.logger.debug("/auth/confirm/new -> User not found")
        pass
    else:
        if u.is_confirmed:
            current_app.logger.debug("/auth/confirm/new -> User found, Already confirmed.")
            pass
        else:
            current_app.logger.debug("/auth/confirm/new -> User found, sending new confirmation email")
            token = generate_confirmation_token(email=email, token_type="confirm")
            send_mail_text.delay(
                dest=data["email"],
                subject="Confirm your email for PyMatcha",
                body=os.getenv("APP_URL") + "/auth/confirm/" + token,
            )
    current_app.logger.debug("/auth/confirm/new -> New confirmation email sent if user exists in database")
    return Success("New confirmation email sent if user exists in database")
