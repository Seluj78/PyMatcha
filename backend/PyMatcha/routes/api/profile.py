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

import flask_jwt_extended as fjwt
import PyMatcha.models.user as user
from flask import Blueprint
from flask import request
from PyMatcha.errors import BadRequestError
from PyMatcha.models.tag import Tag
from PyMatcha.success import Success
from PyMatcha.utils.decorators import validate_params

User = user.User
get_user = user.get_user

profile_bp = Blueprint("profile", __name__)

REQUIRED_PARAMS_COMPLETE_PROFILE = {"gender": str, "birthdate": int, "orientation": str, "bio": str, "tags": list}


@profile_bp.route("/profile/complete", methods=["POST"])
@fjwt.jwt_required
@validate_params(REQUIRED_PARAMS_COMPLETE_PROFILE)
def complete_profile():
    current_user = fjwt.current_user
    if current_user.is_profile_completed:
        raise BadRequestError(
            "The user has already completed his profile", "Go to your profile settings to edit your profile"
        )
    data = request.get_json()
    orientation = data["orientation"]
    bio = data["bio"]
    tags = data["tags"]
    gender = data["gender"]
    birthdate = data["birthdate"]

    if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
        raise BadRequestError("Orientation must be heterosexual, homosexual, bisexual or other", "Try again")

    if gender not in ["male", "female", "other"]:
        raise BadRequestError("Gender must be male, female or other", "Try again")

    for tag in tags:
        Tag.create(name=tag, user_id=current_user.id)

    current_user.orientation = orientation
    current_user.bio = bio
    current_user.is_profile_completed = True
    current_user.gender = gender
    current_user.birthdate = datetime.date.fromtimestamp(int(birthdate))
    current_user.save()
    return Success("Profile completed !")
