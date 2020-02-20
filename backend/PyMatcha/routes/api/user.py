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

from flask import Blueprint, jsonify

from PyMatcha.models import User, get_user
from PyMatcha.errors import NotFoundError


user_bp = Blueprint("user", __name__)


@user_bp.route("/users/", methods=["GET"])
def get_all_users():
    user_list = []
    for user in User.select_all():
        user_list.append(user.get_all_info())
    return jsonify(user_list)


@user_bp.route("/users/<uid>", methods=["GET"])
def get_one_user(uid):
    try:
        user = get_user(uid)
    except NotFoundError:
        raise NotFoundError("User {} not found".format(uid), "Check given uid and try again")
    else:
        return jsonify(user.get_all_info())