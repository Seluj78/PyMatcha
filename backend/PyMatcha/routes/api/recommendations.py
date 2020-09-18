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

from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha import redis
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import SuccessOutput

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations", methods=["GET"])
@jwt_required
def get_recommendations():
    recommendations = redis.get(f"user_recommendations:{str(current_user.id)}")
    if not recommendations:
        raise NotFoundError("Recommendations not calculated yet", "Please come back later")
    return SuccessOutput("recommendations", json.loads(recommendations))
