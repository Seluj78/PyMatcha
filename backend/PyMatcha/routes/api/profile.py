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
import PyMatcha.models.user as user
from flask import Blueprint
from flask import request
from PyMatcha.errors import BadRequestError
from PyMatcha.success import Success
from PyMatcha.utils.decorators import validate_params

User = user.User
get_user = user.get_user

profile_bp = Blueprint("profile", __name__)

REQUIRED_PARAMS_COMPLETE_PROFILE = {
    "genre": str,
    "bio": str,
    # "tags": str
}


@profile_bp.route("/profile/complete")
@fjwt.jwt_required
@validate_params(REQUIRED_PARAMS_COMPLETE_PROFILE)
def complete_profile():
    current_user = fjwt.current_user
    data = request.json()
    genre = data["genre"]
    bio = data["bio"]

    if genre not in ["heterosexual", "homosexual", "bisexual", "other"]:
        raise BadRequestError("Genre must be heterosexual, homosexual, bisexual or other", "Try again")

    current_user.genre = genre
    current_user.bio = bio
    current_user.is_profile_completed = True
    current_user.save()
    return Success("Profile completed !")
