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


REQUIRED_KEYS_NEW_MESSAGE = {"to_uid": str, "content": str}

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/conversations", methods=["GET"])
@jwt_required
def get_opened_conversations():
    conv_list = current_user.get_conversation_list()
    returned_list = [
        {
            "last_message_timestamp": c.timestamp,
            "last_message_content": c.content,
            "is_unseen": True if not c.is_seen and c.to_id == current_user.id else False,
            "with_user": get_user(c.to_id if c.to_id != current_user.id else c.from_id).to_dict(),
        }
        for c in conv_list
    ]
    return SuccessOutput("conversations", returned_list)


@messages_bp.route("/messages/send", methods=["POST"])
@validate_params(REQUIRED_KEYS_NEW_MESSAGE)
@jwt_required
def send_message():
    current_app.logger.debug("/messages -> Call")
    data = request.get_json()
    to_uid: str = data["to_uid"]
    content: str = data["content"]
    try:
        to_user = get_user(to_uid)
    except NotFoundError:
        raise NotFoundError(f"Recipient {to_uid} not found.")

    if current_user.id == to_user.id:
        raise BadRequestError("Cannot send a message to yourself.")

    current_user.send_message(to_id=to_user.id, content=content)
    current_app.logger.debug("/messages -> Message successfully sent to {}.".format(to_uid))
    return Success("Message successfully sent to {}.".format(to_uid))


@messages_bp.route("/conversations/<with_uid>", methods=["GET"])
@jwt_required
def get_conversation_messsages(with_uid):
    try:
        with_user = get_user(with_uid)
    except NotFoundError:
        raise NotFoundError("With user {} not found.")

    if with_user.id == current_user.id:
        raise BadRequestError("Cannot get conversation with yourself. Get a life...")

    message_list = current_user.get_messages_with_user(with_user.id)
    message_list = [m.to_dict() for m in message_list]
    return SuccessOutput("messages", message_list)


@messages_bp.route("/messages/see/<with_uid>", methods=["POST"])
@jwt_required
def see_conversation_messages(with_uid):
    try:
        with_user = get_user(with_uid)
    except NotFoundError:
        raise NotFoundError(f"With user {with_uid} not found.")
    unseen_messages = Message.get_multis(from_id=with_user.id, to_id=current_user.id, is_seen=False)
    for message in unseen_messages:
        message.is_seen = True
        message.seen_timestamp = datetime.datetime.utcnow()
        message.save()
    return Success("Messages marked as seen.")


@messages_bp.route("/messages/like/<message_id>", methods=["POST"])
@jwt_required
def like_message(message_id):
    message = Message.get(id=message_id)
    if not message:
        raise NotFoundError(f"Message {message_id} not found.")
    if message.from_id == current_user.id:
        raise BadRequestError("Cannot like your own message.")
    if message.to_id != current_user.id:
        raise BadRequestError("Cannot like a message that isn't destined to you.")
    if message.is_liked:
        raise BadRequestError("Message is already liked.")
    message.is_liked = True
    message.save()
    return Success(f"Liked message {message_id}.")


@messages_bp.route("/messages/unlike/<message_id>", methods=["POST"])
@jwt_required
def unlike_message(message_id):
    message = Message.get(id=message_id)
    if not message:
        raise NotFoundError(f"Message {message_id} not found.")
    if message.from_id == current_user.id:
        raise BadRequestError("Cannot unlike your own message.")
    if message.to_id != current_user.id:
        raise BadRequestError("Cannot unlike a message that isn't destined to you.")
    if not message.is_liked:
        raise BadRequestError("Message is already unliked.")
    message.is_liked = False
    message.save()
    return Success(f"Unliked message {message_id}.")


@messages_bp.route("/messages/unseen", methods=["GET"])
@jwt_required
def get_new_messages():
    message_list = Message.get_multis(to_id=current_user.id, is_seen=False)
    new_messages = [m.to_dict() for m in message_list]
    return SuccessOutput("new_messages", new_messages)
