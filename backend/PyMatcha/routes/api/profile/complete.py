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
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha import redis
from PyMatcha.models.tag import Tag
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.success import Success

profile_complete_bp = Blueprint("profile_complete", __name__)

REQUIRED_PARAMS_COMPLETE_PROFILE = {"gender": str, "birthdate": str, "orientation": str, "bio": str, "tags": list}


@profile_complete_bp.route("/profile/complete", methods=["POST"])
@validate_params(REQUIRED_PARAMS_COMPLETE_PROFILE)
@jwt_required
def complete_profile():
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

    try:
        birthdate = datetime.datetime.strptime(birthdate, "%d/%m/%Y").date()
    except ValueError:
        raise BadRequestError("Birthdate format must be %d/%m/%Y (day/month/year)")

    if len(bio) <= 50:
        raise BadRequestError("Bio is too short.")

    if len(tags) < 3:
        raise BadRequestError("At least 3 tags are required.")

    if len(tags) != len(set(tags)):
        raise BadRequestError("Duplicate tags.")

    today = datetime.datetime.utcnow()

    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18:
        raise BadRequestError("You must be 18 years old or older.")

    for tag in tags:
        Tag.create(name=tag, user_id=current_user.id)

    current_user.orientation = orientation
    current_user.bio = bio
    current_user.is_profile_completed = True
    current_user.gender = gender
    current_user.birthdate = birthdate
    current_user.save()
    redis.set(f"superlikes:{current_user.id}", 5)
    return Success("Profile completed !")
