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
from flask import Blueprint
from flask import current_app
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.message import Message
from PyMatcha.models.user import get_user
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput


REQUIRED_KEYS_NEW_MESSAGE = {"to_id": int, "content": str}
# REQUIRED_KEYS_GET_CONVERSATION = {"with_id": int}

messages_bp = Blueprint("messages", __name__)

# TODO: Route to get the last message for each open conversation
# TODO: Route to send a new message to a conversation

"""
Route to get latest messages with user (then paginated to get the older messages)
route to receive messages
"""


@messages_bp.route("/conversations", methods=["GET"])
@jwt_required
def get_opened_conversations():
    conv_list = current_user.get_conversation_list()
    returned_list = [c.to_dict() for c in conv_list]
    return SuccessOutput("conversations", returned_list)


@messages_bp.route("/messages/see/<with_uid>", methods=["POST"])
@jwt_required
def see_conversation_messages(with_uid):
    try:
        with_user = get_user(with_uid)
    except NotFoundError:
        raise NotFoundError("With user {} not found", "Try again")
    for message in Message.get_multis(from_id=with_user.id, to_id=current_user.id, is_seen=False):
        message.is_seen = True
        message.save()
    return Success("Messages marked as seen")


@messages_bp.route("/messages/like/<message_id>", methods=["POSt"])
@jwt_required
def like_message(message_id):
    try:
        message = Message.get(message_id)
    except NotFoundError:
        raise NotFoundError(f"Message {message_id} not found", "Try again")
    if message.to_id != current_user.id:
        raise BadRequestError("Cannot like a message that isn't destined to you", "Try again")
    message.is_liked = True
    message.save()
    return Success(f"Liked message {message_id}")


@messages_bp.route("/messages/send", methods=["POST"])
@jwt_required
@validate_params(REQUIRED_KEYS_NEW_MESSAGE)
def send_message():
    current_app.logger.debug("/messages -> Call")
    data = request.get_json()
    to_id: int = int(data["to_id"])
    content: str = data["content"]
    try:
        get_user(to_id)
    except NotFoundError:
        raise NotFoundError("Recipient {} not found", "Try again")
    current_user.send_message(to_id=to_id, content=content)
    current_app.logger.debug("/messages -> Message successfully sent to {}".format(to_id))
    return Success("Message successfully sent to {}".format(to_id))


# @messages_bp.route("/messages/conversation", methods=["GET"])
# @jwt_required
# @validate_params(REQUIRED_KEYS_GET_CONVERSATION)
# def get_conversation():
#     data = request.get_json()
#     with_id: int = int(data["with_id"])
#     return SuccessOutput("messages", current_user.get_messages_with_user(with_id))
