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

from flask import Blueprint, jsonify, request

from werkzeug.exceptions import BadRequest

from PyMatcha.models import User, get_user
from PyMatcha.errors import NotFoundError, BadRequestError, ConflictError
from PyMatcha.success import SuccessOutputMessage


REQUIRED_KEYS_USER_CREATION = ["username", "email", "password"]


user_bp = Blueprint("user", __name__)


@user_bp.route("/users/", methods=["GET"])
def get_all_users():
    user_list = []
    for user in User.select_all():
        user_list.append(user.get_all_info())
    return jsonify(user_list)


@user_bp.route("/users/<uid>", methods=["GET"])
def get_one_user(uid):
    try:
        user = get_user(uid)
    except NotFoundError:
        raise NotFoundError("User {} not found".format(uid), "Check given uid and try again")
    else:
        return jsonify(user.get_all_info())


@user_bp.route("/auth/register", methods=["POST"])
def api_create_user():
    # If the json body is missing something (`,` for example), throw an error
    try:
        data = request.get_json()
    except BadRequest:
        raise BadRequestError("The Json Body is malformed", "Please check it and try again")

    # If the data dict is empty
    if not data:
        raise BadRequestError("Missing json body.", "Please fill your json body")

    missing = []
    for item in REQUIRED_KEYS_USER_CREATION:
        # If a key is missing in the sent data
        if item not in data.keys():
            missing.append(item)
    if missing:
        raise BadRequestError(
            "Missing keys {} to create user.".format(missing), "Complete your json body and try again"
        )

    for item in data.keys():
        # If there's an unwanted key in the sent data
        if item not in REQUIRED_KEYS_USER_CREATION:
            raise BadRequestError(
                "You can't specify key '{}'.".format(item),
                "You are only allowed to specify the fields {} " "when creating a user.".format(request),
            )

    for key, value in data.items():
        if value is None or value == "":
            raise BadRequestError(f"The item {key} cannot be None or empty", "Please try again.")

    data["email"] = data["email"].lower()

    try:
        new_user = User.register(email=data["email"], username=data["username"], password=data["password"])
    except ConflictError as e:
        raise e
    else:
        return SuccessOutputMessage("email", new_user.email, "New user successfully created.")
