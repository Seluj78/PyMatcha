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
import logging

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.utils.errors import NotFoundError


user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
@jwt_required
def get_all_users():
    user_list = []
    for u in User.select_all():
        user_list.append(u.to_dict())
    logging.info("Returning all users list")
    return jsonify(user_list)


@user_bp.route("/users/<uid>", methods=["GET"])
@jwt_required
def get_one_user(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        pass
    else:
        logging.info(f"Returning info on user {uid}")
        return jsonify(u.to_dict())


@user_bp.route("/users/online", methods=["GET"])
@jwt_required
def get_all_online_users():
    online_user_list = []
    for user in User.get_multis(is_online=True):
        online_user_list.append(user.to_dict())
    logging.info("Returning list of online users")
    return jsonify(online_user_list)
