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

from flask import Blueprint, request


import flask_jwt_extended as fjwt

import PyMatcha.models.user as user

from PyMatcha.errors import NotFoundError
from PyMatcha.success import Success
from PyMatcha.utils.decorators import validate_required_params

REQUIRED_KEYS_NEW_MESSAGE = ["to_id", "content"]


messages_bp = Blueprint("messages", __name__)

# TODO: Route to get messages since X timestamp


@messages_bp.route("/messages", methods=["POST"])
@fjwt.jwt_required
@validate_required_params(REQUIRED_KEYS_NEW_MESSAGE)
def send_message():
    data = request.get_json()
    to_id: int = int(data["to_id"])
    content: str = data["content"]
    current_user = fjwt.get_current_user()
    try:
        sender = user.get_user(current_user["id"])
    except NotFoundError:
        raise NotFoundError("User {} (from_id) not found.".format(current_user["id"]), "Try again with another uid")
    sender.send_message(to_id=to_id, content=content)
    return Success("Message successfully sent to {}".format(to_id))
