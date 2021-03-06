"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/gmorer
    <jlasne@student.42.fr> - <lauris.skraucis@gmail.com>

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
import logging

from flask import Blueprint
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jti
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required
from PyMatcha import ACCESS_TOKEN_EXPIRES
from PyMatcha import redis
from PyMatcha import REFRESH_TOKEN_EXPIRES
from PyMatcha.models.user import get_user
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.errors import UnauthorizedError
from PyMatcha.utils.mail import send_mail_text
from PyMatcha.utils.password import check_password
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput

REQUIRED_KEYS_LOGIN = {"username": str, "password": str}

auth_login_bp = Blueprint("auth_login", __name__)


@auth_login_bp.route("/auth/login", methods=["POST"])
@validate_params(REQUIRED_KEYS_LOGIN)
def auth_login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    try:
        u = get_user(username)
    except NotFoundError:
        logging.debug("User not found for login")
        raise UnauthorizedError("Incorrect username or password.")
    if not check_password(u.password, password):
        logging.debug("Password invalid for login")
        raise UnauthorizedError("Incorrect username or password.")

    if not u.is_confirmed:
        logging.debug("User is trying to login unconfirmed")
        raise UnauthorizedError("User needs to be confirmed first.", "Try again when you have confirmed your email.")
    logging.debug(f"Creating token for {u.id}")
    access_token = create_access_token(identity=u.get_jwt_info(), fresh=True)
    refresh_token = create_refresh_token(identity=u.get_jwt_info())
    access_jti = get_jti(access_token)
    refresh_jti = get_jti(refresh_token)

    redis.set("is_revoked_jti:" + access_jti, "false", ACCESS_TOKEN_EXPIRES * 1.2)
    redis.set("is_revoked_jti:" + refresh_jti, "false", REFRESH_TOKEN_EXPIRES * 1.2)

    logging.debug("Returning access token for user {}".format(username))
    u.is_online = True
    u.dt_lastseen = datetime.datetime.utcnow()
    u.save()
    send_mail_text.delay(
        dest=u.email,
        subject="[Matcha] Login notification",
        body=f"Someone logged in into your account at {datetime.datetime.utcnow()}."
        f"If you believe it wasn't you, please change your password immediately!",
    )
    ret = {"access_token": access_token, "refresh_token": refresh_token, "is_profile_completed": u.is_profile_completed}
    return SuccessOutput("return", ret)


@auth_login_bp.route("/auth/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    logging.info(f"Refreshing token for {current_user['id']}")
    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)
    redis.set("is_revoked_jti:" + access_jti, "false", ACCESS_TOKEN_EXPIRES * 1.2)
    return SuccessOutput("access_token", access_token)


@auth_login_bp.route("/auth/logout", methods=["POST"])
@validate_params({"access_token": str, "refresh_token": str})
def logout():
    data = request.get_json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    access_jti = get_jti(access_token)
    refresh_jti = get_jti(refresh_token)
    redis.set("is_revoked_jti:" + access_jti, "true", ACCESS_TOKEN_EXPIRES * 1.2)
    redis.set("is_revoked_jti:" + refresh_jti, "true", REFRESH_TOKEN_EXPIRES * 1.2)
    logging.info(f"Revoked tokens with jtis {access_jti}, {refresh_jti}")
    return Success("Logout successful.")
