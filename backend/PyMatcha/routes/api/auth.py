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

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jti
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from PyMatcha import ACCESS_TOKEN_EXPIRES
from PyMatcha import redis
from PyMatcha import REFRESH_TOKEN_EXPIRES
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.utils import hash_password
from PyMatcha.utils.confirm_token import confirm_token
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import ConflictError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.errors import UnauthorizedError
from PyMatcha.utils.mail import send_mail_text
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput
from PyMatcha.utils.success import SuccessOutputMessage


REQUIRED_KEYS_USER_CREATION = {"username": str, "email": str, "password": str, "first_name": str, "last_name": str}
REQUIRED_KEYS_PASSWORD_FORGOT = {"email": str}
REQUIRED_KEYS_PASSWORD_RESET = {"token": str, "password": str}
REQUIRED_KEYS_LOGIN = {"username": str, "password": str}
REQUIRED_KEYS_NEW_EMAIL_CONF = {"email": str}

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
@validate_params(REQUIRED_KEYS_USER_CREATION)
def api_create_user():
    current_app.logger.debug("/auth/register -> Call")
    data = request.get_json()
    data["email"] = data["email"].lower()
    try:
        current_app.logger.debug("Trying to register new user {}, {}".format(data["email"], data["username"]))
        new_user = User.register(
            email=data["email"],
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
    except ConflictError as e:
        current_app.logger.error("Conflict error on user register: {}".format(e))
        raise e
    else:
        token = generate_confirmation_token(email=data["email"], token_type="confirm")
        send_mail_text.delay(
            dest=data["email"],
            subject="Confirm your email for PyMatcha",
            body=os.getenv("APP_URL") + "/auth/confirm/" + token,
        )
        current_app.logger.debug("New user {} successfully created".format(new_user.email))
        return SuccessOutputMessage("email", new_user.email, "New user successfully created.")


@auth_bp.route("/auth/confirm/<token>", methods=["GET"])
def confirm_email(token):
    current_app.logger.debug("/auth/confirm/{} -> Call".format(token))
    try:
        email, token_type = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            current_app.logger.debug("/auth/confirm -> Signature Expired")
            return redirect("/?type=confirm&success=false&message=Signature expired")
        else:
            current_app.logger.debug("/auth/confirm -> Bad Expired")
            return redirect("/?type=confirm&success=false&message=Bad Signature")
    else:
        if token_type != "confirm":
            current_app.logger.debug("/auth/confirm -> Wrong token type")
            return redirect("/?type=confirm&success=false&message=Wrong token type")
        try:
            u = get_user(email)
        except NotFoundError:
            current_app.logger.debug("/auth/confirm -> User not found")
            return redirect("/?type=confirm&success=false&message=User not found")
        if u.is_confirmed:
            current_app.logger.debug("/auth/confirm -> User already confirmed")
            return redirect("/?type=confirm&success=false&message=User already confirmed")
        else:
            u.is_confirmed = True
            u.confirmed_on = datetime.datetime.utcnow()
            u.save()
        current_app.logger.debug("/auth/confirm -> User {} confirmed.".format(u.id))
        return redirect("/?type=confirm&success=true&message=User confirmed")


@auth_bp.route("/auth/password/forgot", methods=["POST"])
@validate_params(REQUIRED_KEYS_PASSWORD_FORGOT)
def forgot_password():
    current_app.logger.debug("/auth/password/forgot -> Call")
    data = request.get_json()
    try:
        get_user(data["email"])
    except NotFoundError:
        current_app.logger.debug("/auth/password/forgot -> User {} not found, no email sent".format(data["email"]))
        pass
    else:
        token = generate_confirmation_token(email=data["email"], token_type="reset")
        current_app.logger.debug("/auth/password/forgot -> Sending worker request to send email")
        send_mail_text.delay(
            dest=data["email"],
            subject="Password reset for PyMatcha",
            body=os.getenv("APP_URL") + "/reset_password?token=" + token,
        )
    current_app.logger.debug(
        "/auth/password/forgot -> Password reset mail sent successfully for user {}".format(data["email"])
    )
    return Success("Password reset mail sent successfully if user exists in DB")


@auth_bp.route("/auth/password/reset", methods=["POST"])
@validate_params(REQUIRED_KEYS_PASSWORD_RESET)
def reset_password():
    current_app.logger.debug("/auth/password/reset -> Call")
    data = request.get_json()
    try:
        email, token_type = confirm_token(data["token"], expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            current_app.logger.debug("/auth/password/reset -> Signature Expired")
            raise BadRequestError("Signature Expired.", "Request another password reset and try again.")
        else:
            current_app.logger.debug("/auth/password/reset -> Bad Signature")
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        if token_type != "reset":
            current_app.logger.debug("/auth/password/reset -> Wrong token type")
            raise BadRequestError("Wrong token type", "Try again with the correct type")
        try:
            u = get_user(email)
        except NotFoundError:
            current_app.logger.debug("/auth/password/reset -> User not found")
            raise NotFoundError("User not found", "Try again with another user.")
        if u.previous_reset_token == data["token"]:
            current_app.logger.debug("/auth/password/reset -> Token already used")
            raise BadRequestError("Token already used", "Please request a new one")
        u.password = hash_password(data["password"])
        u.previous_reset_token = data["token"]
        u.save()
        current_app.logger.debug("/auth/password/reset -> Password reset successfully")
        return Success("Password reset successful")


@auth_bp.route("/auth/login", methods=["POST"])
@validate_params(REQUIRED_KEYS_LOGIN)
def auth_login():
    current_app.logger.debug("/auth/login -> Call")
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    try:
        u = get_user(username)
    except NotFoundError:
        current_app.logger.debug("/auth/login -> User not found")
        raise UnauthorizedError("Incorrect username or password", "Try again")
    if not u.check_password(password):
        current_app.logger.debug("/auth/login -> Password invalid")
        raise UnauthorizedError("Incorrect username or password", "Try again")

    if not u.is_confirmed:
        current_app.logger.debug("/auth/login -> User is trying to login unconfirmed")
        raise UnauthorizedError("User needs to be confirmed first.", "Try again when you have confirmed your email")
    access_token = create_access_token(identity=u.get_jwt_info(), fresh=True)
    refresh_token = create_refresh_token(identity=u.get_jwt_info())
    access_jti = get_jti(access_token)
    refresh_jti = get_jti(refresh_token)

    redis.set("jti:" + access_jti, "false", ACCESS_TOKEN_EXPIRES * 1.2)
    redis.set("jti:" + refresh_jti, "false", REFRESH_TOKEN_EXPIRES * 1.2)

    current_app.logger.debug("/auth/login -> Returning access token for user {}".format(username))
    redis.set("user:" + str(u.id), datetime.datetime.utcnow().timestamp())
    ret = {"access_token": access_token, "refresh_token": refresh_token, "is_profile_completed": u.is_profile_completed}
    return SuccessOutput("return", ret)


@auth_bp.route("/auth/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)
    redis.set("jti:" + access_jti, "false", ACCESS_TOKEN_EXPIRES * 1.2)
    return SuccessOutput("access_token", access_token)


@auth_bp.route("/auth/access_revoke", methods=["DELETE"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    redis.set("jti:" + jti, "true", ACCESS_TOKEN_EXPIRES * 1.2)
    return Success("Access token revoked")


@auth_bp.route("/auth/refresh_revoke", methods=["DELETE"])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()["jti"]
    redis.set("jti:" + jti, "true", REFRESH_TOKEN_EXPIRES * 1.2)
    return Success("Refresh token revoked")


@auth_bp.route("/auth/confirm/new", methods=["POST"])
@validate_params(REQUIRED_KEYS_NEW_EMAIL_CONF)
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
            return Success("User already confirmed")
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
