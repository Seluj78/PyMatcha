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
import json
import logging

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha import redis
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.recommendations import create_user_recommendations
from PyMatcha.utils.success import SuccessOutput

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations", methods=["GET"])
@jwt_required
def get_recommendations():
    logging.info(f"Getting recommendations for user {current_user.id}")
    force = request.args.get("force", default=False, type=bool)
    recommendations = redis.get(f"user_recommendations:{str(current_user.id)}")
    if force or not recommendations:
        create_user_recommendations(current_user)
        recommendations = redis.get(f"user_recommendations:{str(current_user.id)}")
        if not recommendations:
            raise BadRequestError("User recommendations cannot be calculated.")
    return SuccessOutput("recommendations", json.loads(recommendations))
