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

from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jti
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import jwt_required
from PyMatcha import ACCESS_TOKEN_EXPIRES
from PyMatcha import redis
from PyMatcha import REFRESH_TOKEN_EXPIRES
from PyMatcha.models.user import get_user
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.errors import UnauthorizedError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput


REQUIRED_KEYS_LOGIN = {"username": str, "password": str}

auth_login_bp = Blueprint("auth_login", __name__)


@auth_login_bp.route("/auth/login", methods=["POST"])
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
        raise UnauthorizedError("Incorrect username or password")
    if not u.check_password(password):
        current_app.logger.debug("/auth/login -> Password invalid")
        raise UnauthorizedError("Incorrect username or password")

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


@auth_login_bp.route("/auth/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    access_jti = get_jti(encoded_token=access_token)
    redis.set("jti:" + access_jti, "false", ACCESS_TOKEN_EXPIRES * 1.2)
    return SuccessOutput("access_token", access_token)


@auth_login_bp.route("/auth/access_revoke", methods=["DELETE"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    redis.set("jti:" + jti, "true", ACCESS_TOKEN_EXPIRES * 1.2)
    return Success("Access token revoked")


@auth_login_bp.route("/auth/refresh_revoke", methods=["DELETE"])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()["jti"]
    redis.set("jti:" + jti, "true", REFRESH_TOKEN_EXPIRES * 1.2)
    return Success("Refresh token revoked")
