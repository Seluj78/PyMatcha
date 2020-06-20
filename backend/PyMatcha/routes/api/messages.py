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
import PyMatcha.models.user as user
from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput

REQUIRED_KEYS_NEW_MESSAGE = {"to_id": int, "content": str}
REQUIRED_KEYS_GET_CONVERSATION = {"with_id": int}

messages_bp = Blueprint("messages", __name__)

# TODO: Route to get the last message for each open conversation
# TODO: Route to get latest messages with user (then paginated to get the older messages)
# TODO: Route to send a new message to a conversation


@messages_bp.route("/messages/send/", methods=["POST"])
@jwt_required
@validate_params(REQUIRED_KEYS_NEW_MESSAGE)
def send_message():
    current_app.logger.debug("/messages -> Call")
    data = request.get_json()
    to_id: int = int(data["to_id"])
    content: str = data["content"]
    try:
        sender = user.get_user(current_user.id)
    except NotFoundError:
        raise NotFoundError("User {} (from_id) not found.".format(current_user.id), "Try again with another uid")
    sender.send_message(to_id=to_id, content=content)
    current_app.logger.debug("/messages -> Message successfully sent to {}".format(to_id))
    return Success("Message successfully sent to {}".format(to_id))


@messages_bp.route("/messages/conversation/", methods=["GET"])
@jwt_required
@validate_params(REQUIRED_KEYS_GET_CONVERSATION)
def get_conversation():
    data = request.get_json()
    with_id: int = int(data["with_id"])
    return SuccessOutput("messages", current_user.get_messages_with_user(with_id))
