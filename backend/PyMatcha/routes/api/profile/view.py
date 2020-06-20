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
from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.user import get_user
from PyMatcha.models.view import View
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import SuccessOutput

profile_view_bp = Blueprint("profile_view", __name__)


@profile_view_bp.route("/profile/views", methods=["GET"])
@jwt_required
def get_profile_views():
    profile_views = current_user.get_views()
    profile_views = [v.to_dict() for v in profile_views]
    return SuccessOutput("views", profile_views)


@profile_view_bp.route("/profile/view/<uid>", methods=["GET"])
@jwt_required
def view_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found", "try again")

    if current_user.id != u.id:
        View.create(profile_id=u.id, viewer_id=current_user.id)

    return SuccessOutput("profile", u.to_dict())
