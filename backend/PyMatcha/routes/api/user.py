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
import flask_jwt_extended as fjwt
from flask import Blueprint
from flask import current_app
from flask import jsonify
from PyMatcha import redis
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.utils.errors import NotFoundError


user_bp = Blueprint("user", __name__)


@user_bp.route("/users/", methods=["GET"])
@fjwt.jwt_required
def get_all_users():
    current_app.logger.info("/users/ -> Call")
    user_list = []
    for u in User.select_all():
        user_list.append(u.to_dict())
    current_app.logger.info("/users/ -> Returning all users list")
    return jsonify(user_list)


@user_bp.route("/users/<uid>", methods=["GET"])
@fjwt.jwt_required
def get_one_user(uid):
    current_app.logger.info("/users/{} -> Call".format(uid))
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError("User {} not found".format(uid), "Check given uid and try again")
    else:
        current_app.logger.info("/users/{} -> Returning info on user {}".format(uid, uid))
        return jsonify(u.to_dict())


@user_bp.route("/users/online", methods=["GET"])
@fjwt.jwt_required
def get_all_online_users():
    user_id = None  # noqa
    date_lastseen = None  # noqa
    online_user_list = []
    for key in redis.scan_iter("user:*"):
        user_id = str(key).split(":")[1]
        date_lastseen = float(redis.get(key))
        online_user_list.append({"id": user_id, "date_lastseen": date_lastseen})
    return jsonify(online_user_list)
