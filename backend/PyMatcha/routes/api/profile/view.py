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
from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.user import get_user
from PyMatcha.utils.action_notifs.view import do_view
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.success import SuccessOutput

profile_view_bp = Blueprint("profile_view", __name__)


@profile_view_bp.route("/profile/view/<uid>", methods=["GET"])
@jwt_required
def view_profile(uid):
    try:
        viewed_user = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == viewed_user.id:
        raise BadRequestError("Cannot view yourself.")
    do_view(viewer_user=current_user, viewed_user_id=viewed_user.id)

    user_dict = viewed_user.to_dict()
    # TODO: Update swagger with this
    user_dict["distance"] = _get_distance(current_user.geohash, viewed_user.geohash)
    return SuccessOutput("profile", user_dict)
