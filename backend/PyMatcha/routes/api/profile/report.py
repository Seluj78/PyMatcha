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
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.report import Report
from PyMatcha.models.user import get_user
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success

profile_report_bp = Blueprint("profile_report", __name__)


@profile_report_bp.route("/profile/report/<uid>", methods=["POST"])
@validate_params({"reason": str})
@jwt_required
def report_profile(uid):
    data = request.get_json()
    reason = data["reason"]

    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == u.id:
        raise BadRequestError("Cannot report yourself.")

    if reason not in ["harassment", "bot", "spam", "inappropriate content"]:
        raise BadRequestError("Reason must be 'harassment', 'bot', 'spam' or 'inappropriate content'.")

    details = None
    Report.create(reporter_id=current_user.id, reported_id=u.id, reason=reason, details=details)

    return Success(f"Report created on user {u.email}.")
