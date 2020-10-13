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
import datetime

import Geohash
import requests
from flask import Blueprint
from flask import render_template
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.tag import Tag
from PyMatcha.models.user import get_user
from PyMatcha.utils import hash_password
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.errors import UnauthorizedError
from PyMatcha.utils.mail import send_mail_html
from PyMatcha.utils.mail import send_mail_text
from PyMatcha.utils.password import check_password
from PyMatcha.utils.static import FRONTEND_EMAIL_CONFIRMATION_URL
from PyMatcha.utils.success import Success

profile_edit_bp = Blueprint("profile_edit", __name__)


@profile_edit_bp.route("/profile/edit/first_name", methods=["PATCH"])
@validate_params({"first_name": str})
@jwt_required
def edit_profile_first_name():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    first_name = data["first_name"]
    current_user.first_name = first_name
    current_user.save()
    return Success("First name successfully modified!")


@profile_edit_bp.route("/profile/edit/last_name", methods=["PATCH"])
@validate_params({"last_name": str})
@jwt_required
def edit_profile_last_name():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    last_name = data["last_name"]
    current_user.last_name = last_name
    current_user.save()
    return Success("Last name successfully modified!")


@profile_edit_bp.route("/profile/edit/username", methods=["PATCH"])
@validate_params({"username": str})
@jwt_required
def edit_profile_username():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    username = data["username"]
    try:
        get_user(username)
    except NotFoundError:
        pass
    else:
        raise BadRequestError("Username taken.")
    current_user.username = username
    current_user.save()
    return Success("Username successfully modified!")


@profile_edit_bp.route("/profile/edit/bio", methods=["PATCH"])
@validate_params({"bio": str})
@jwt_required
def edit_profile_bio():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    bio = data["bio"]
    if len(bio) <= 50:
        raise BadRequestError("Bio is too short.")
    current_user.bio = bio
    current_user.save()
    return Success("Bio successfully modified!")


@profile_edit_bp.route("/profile/edit/gender", methods=["PATCH"])
@validate_params({"gender": str})
@jwt_required
def edit_profile_gender():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    gender = data["gender"]
    if gender not in ["male", "female", "other"]:
        raise BadRequestError("Gender must be male, female or other.")
    current_user.gender = gender
    current_user.save()
    return Success("Gender successfully modified!")


@profile_edit_bp.route("/profile/edit/orientation", methods=["PATCH"])
@validate_params({"orientation": str})
@jwt_required
def edit_profile_orientation():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    orientation = data["orientation"]
    if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
        raise BadRequestError("Orientation must be heterosexual, homosexual, bisexual or other.")
    current_user.orientation = orientation
    current_user.save()
    return Success("Orientation successfully modified!")


@profile_edit_bp.route("/profile/edit/birthdate", methods=["PATCH"])
@validate_params({"birthdate": str})
@jwt_required
def edit_profile_birthdate():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    birthdate = data["birthdate"]
    try:
        birthdate = datetime.datetime.strptime(birthdate, "%d/%m/%Y").date()
    except ValueError:
        raise BadRequestError("Birthdate format must be %d/%m/%Y (day/month/year).")

    today = datetime.datetime.utcnow()

    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 18:
        raise BadRequestError("You must be 18 years old or older.")
    current_user.birthdate = birthdate
    current_user.save()
    return Success("Birthdate successfully modified!")


@profile_edit_bp.route("/profile/edit/tags", methods=["PATCH"])
@validate_params({"tags": list})
@jwt_required
def edit_profile_tags():
    if not current_user.is_profile_completed:
        raise BadRequestError("The user has not completed his profile.", "Complete your profile and try again.")
    data = request.get_json()
    tags = data["tags"]
    current_tags = Tag.get_multis(user_id=current_user.id)
    for t in current_tags:
        t.delete()
    for tag in tags:
        Tag.create(name=tag, user_id=current_user.id)
    return Success("Tags successfully modified!")


@profile_edit_bp.route("/profile/edit/email", methods=["PUT"])
@validate_params({"email": str})
@jwt_required
def edit_email():
    data = request.get_json()
    new_email = data["email"].lower()
    if current_user.email == new_email:
        raise BadRequestError("The new email is the same as the old one !")
    current_user.email = new_email
    current_user.is_confirmed = False
    current_user.save()
    token = generate_confirmation_token(email=new_email, token_type="confirm")
    link = FRONTEND_EMAIL_CONFIRMATION_URL + token
    rendered_html = render_template("confirm_email.html", link=link)
    send_mail_html.delay(dest=data["email"], subject="Confirm your email on PyMatcha", html=rendered_html)
    return Success("Email sent for new email")


@profile_edit_bp.route("/profile/edit/password", methods=["PUT"])
@validate_params({"old_password": str, "new_password": str})
@jwt_required
def edit_password():
    data = request.get_json()
    old_password = data["old_password"]
    new_password = data["new_password"]
    if not check_password(current_user.password, old_password):
        raise UnauthorizedError("Incorrect password.")
    current_user.password = hash_password(new_password)
    current_user.save()
    send_mail_text.delay(
        dest=current_user.email,
        subject="Password change notification",
        body=f"Your password was changed at {datetime.datetime.utcnow()}."
        f" If you believe it wasn't you, please change it immediatly",
    )
    return Success("User password successfully updated.")


@profile_edit_bp.route("/profile/edit/geolocation", methods=["PUT"])
@validate_params({"ip": str}, {"lat": float, "lng": float})
@jwt_required
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
        response = requests.get(
            f"http://api.ipstack.com/{ip}?access_key=b5f9be2253823006b478da121d1c855b&format=1"
        ).json()
        lat = response["latitude"]
        lng = response["longitude"]
        current_user.geohash = Geohash.encode(lat, lng)
    current_user.save()
    return Success("New location sucessfully saved.")
