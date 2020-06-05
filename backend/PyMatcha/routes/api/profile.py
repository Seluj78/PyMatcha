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
import os

import Geohash
from flask import Blueprint
from flask import render_template
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from ip2geotools.databases.noncommercial import DbIpCity
from PyMatcha.models.report import Report
from PyMatcha.models.tag import Tag
from PyMatcha.models.user import get_user
from PyMatcha.models.view import View
from PyMatcha.utils import hash_password
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.errors import UnauthorizedError
from PyMatcha.utils.mail import send_mail_html
from PyMatcha.utils.mail import send_mail_text
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput

profile_bp = Blueprint("profile", __name__)

REQUIRED_PARAMS_COMPLETE_PROFILE = {"gender": str, "birthdate": int, "orientation": str, "bio": str, "tags": list}
REQUIRED_PARAMS_EDIT_PROFILE = {
    "first_name": str,
    "last_name": str,
    "username": str,
    "bio": str,
    "gender": str,
    "orientation": str,
    "birthdate": int,
    "tags": list,
}


@profile_bp.route("/profile/complete", methods=["POST"])
@jwt_required
@validate_params(REQUIRED_PARAMS_COMPLETE_PROFILE)
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

    for tag in tags:
        Tag.create(name=tag, user_id=current_user.id)

    current_user.orientation = orientation
    current_user.bio = bio
    current_user.is_profile_completed = True
    current_user.gender = gender
    current_user.birthdate = datetime.date.fromtimestamp(int(birthdate))
    current_user.save()
    return Success("Profile completed !")


@profile_bp.route("/profile/edit", methods=["PUT"])
@jwt_required
@validate_params(REQUIRED_PARAMS_EDIT_PROFILE)
def edit_profile():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile", "Complete your profile and try again")
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    username = data["username"]
    bio = data["bio"]
    gender = data["gender"]
    orientation = data["orientation"]
    birthdate = data["birthdate"]

    try:
        get_user(username)
    except NotFoundError:
        pass
    else:
        raise BadRequestError("Username taken", "Try again")

    if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
        raise BadRequestError("Orientation must be heterosexual, homosexual, bisexual or other", "Try again")

    if gender not in ["male", "female", "other"]:
        raise BadRequestError("Gender must be male, female or other", "Try again")

    birthdate = datetime.date.fromtimestamp(birthdate)

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.username = username
    current_user.bio = bio
    current_user.gender = gender
    current_user.orientation = orientation
    current_user.birthdate = birthdate
    current_user.save()
    return Success("User successfully modified !")


@profile_bp.route("/profile/edit/email", methods=["PUT"])
@jwt_required
@validate_params({"email": str})
def edit_email():
    data = request.get_json()
    new_email = data["email"].lower()
    if current_user.email == new_email:
        raise BadRequestError("The new email is the same as the old one !", "Try again")
    current_user.email = new_email
    current_user.is_confirmed = False
    current_user.save()
    token = generate_confirmation_token(email=new_email, token_type="confirm")
    link = os.getenv("APP_URL") + "/auth/confirm/" + token
    rendered_html = render_template("confirm_email.html", link=link)
    send_mail_html.delay(dest=data["email"], subject="Confirm your email on PyMatcha", html=rendered_html)
    return Success("Email sent for new email")


@profile_bp.route("/profile/edit/password", methods=["PUT"])
@jwt_required
@validate_params({"old_password": str, "new_password": str})
def edit_password():
    data = request.get_json()
    old_password = data["old_password"]
    new_password = data["new_password"]
    if not current_user.check_password(old_password):
        raise UnauthorizedError("Incorrect password", "Try again")
    current_user.password = hash_password(new_password)
    current_user.save()
    send_mail_text.delay(
        dest=current_user.email,
        subject="Password change notification",
        body=f"Your password was changed at {datetime.datetime.utcnow()}."
        f" If you believe it wasn't you, please change it immediatly",
    )
    return Success("User password successfully updated.")


@profile_bp.route("/profile/edit/geolocation", methods=["PUT"])
@jwt_required
@validate_params({"ip": str}, {"lat": float, "lng": float})
def edit_geolocation():
    data = request.get_json()
    ip = data["ip"]
    try:
        lat = data["lat"]
        lng = data["lng"]
    except KeyError:
        lat = None
        lng = None

    if lat and lng:
        current_user.geohash = Geohash.encode(lat, lng)
    else:
        response = DbIpCity.get(ip, api_key="free")
        lat = response.latitude
        lng = response.longitude
        current_user.geohash = Geohash.encode(lat, lng)
    current_user.save()
    return Success("New location sucessfully saved.")


@profile_bp.route("/profile/views", methods=["GET"])
@jwt_required
def get_profile_views():
    profile_views = current_user.get_views()
    profile_views = [v.to_dict() for v in profile_views]
    return SuccessOutput("views", profile_views)


@profile_bp.route("/profile/view/<uid>", methods=["GET"])
@jwt_required
def view_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found", "try again")

    if current_user.id != u.id:
        View.create(profile_id=u.id, viewer_id=current_user.id)

    return SuccessOutput("profile", u.to_dict())


@profile_bp.route("/profile/report/<uid>", methods=["POST"])
@validate_params({"reason": str}, {"details": str})
@jwt_required
def report_profile(uid):
    data = request.get_json()
    reason = data["reason"]

    if reason not in ["harassment", "bot", "spam", "inappropriate content"]:
        raise BadRequestError("Reason must be 'harassment', 'bot', 'spam' or 'inappropriate content'", "Try again")

    try:
        details = data["details"]
    except KeyError:
        details = None
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found", "try again")
    if current_user.id == u.id:
        raise BadRequestError("Cannot report yourself", "Try again")
    Report.create(reporter_id=current_user.id, reported_id=u.id, reason=reason, details=details)

    return Success(f"Report created on user {u.email}")
