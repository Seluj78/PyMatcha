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
import logging

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.message import Message
from PyMatcha.models.user import get_user
from PyMatcha.utils.action_notifs.message import do_like_message
from PyMatcha.utils.action_notifs.message import do_message
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput
from PyMatcha.utils.success import SuccessOutputMessage
from PyMatcha.utils.tasks import bot_respond_to_message
from timeago import format as timeago_format

REQUIRED_KEYS_NEW_MESSAGE = {"to_uid": str, "content": str}

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/conversations", methods=["GET"])
@jwt_required
def get_opened_conversations():
    conv_list = current_user.get_conversation_list()
    returned_list = [
        {
            "last_message_id": c.id,
            "last_message_dt_sent": c.dt_sent,
            "last_message_dt_sent_ago": timeago_format(c.dt_sent, datetime.datetime.utcnow()),
            "last_message_content": c.content,
            "is_unseen": True if not c.is_seen and c.to_id == current_user.id else False,
            "with_user": get_user(c.to_id if c.to_id != current_user.id else c.from_id).to_dict(),
        }
        for c in conv_list
    ]
    logging.info(f"Returning conversation list for user {current_user.id}")
    return SuccessOutput("conversations", returned_list)


@messages_bp.route("/messages/send", methods=["POST"])
@validate_params(REQUIRED_KEYS_NEW_MESSAGE)
@jwt_required
def send_message():
    data = request.get_json()
    to_uid: str = data["to_uid"]
    content: str = data["content"]
    try:
        to_user = get_user(to_uid)
    except NotFoundError:
        raise NotFoundError(f"Recipient {to_uid} not found.")

    if current_user.id == to_user.id:
        raise BadRequestError("Cannot send a message to yourself.")

    do_message(from_user=current_user, to_user=to_user, content=content)

    new_message = Message.get_multis(to_id=to_user.id, from_id=current_user.id)[-1]

    if to_user.is_bot:
        new_message.is_seen = True
        new_message.dt_seen = datetime.datetime.utcnow()
        new_message.save()
        logging.debug("Sending worker request to respond to message")
        bot_respond_to_message.delay(bot_id=to_user.id, from_id=current_user.id, message_content=content)
    return SuccessOutputMessage("new_message", new_message.to_dict(), "Message successfully sent.")


@messages_bp.route("/conversations/<with_uid>", methods=["GET"])
@jwt_required
def get_conversation_messsages(with_uid):
    try:
        with_user = get_user(with_uid)
    except NotFoundError:
        raise NotFoundError("With user {} not found.")

    if with_user.id == current_user.id:
        raise BadRequestError("Cannot get conversation with yourself. Get a life...")

    logging.debug(f"Getting messages between {current_user.id} and {with_uid}")
    message_list = current_user.get_messages_with_user(with_user.id)
    message_list = [m.to_dict() for m in message_list]
    message_list = sorted(message_list, key=lambda item: item["dt_sent"])
    return SuccessOutput("messages", message_list)


@messages_bp.route("/messages/see/<with_uid>", methods=["POST"])
@jwt_required
def see_conversation_messages(with_uid):
    try:
        with_user = get_user(with_uid)
    except NotFoundError:
        raise NotFoundError(f"With user {with_uid} not found.")
    unseen_messages = Message.get_multis(from_id=with_user.id, to_id=current_user.id, is_seen=False)
    logging.debug(f"Setting all messages as seen between {current_user.id} and {with_uid}")
    for message in unseen_messages:
        message.is_seen = True
        message.dt_seen = datetime.datetime.utcnow()
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

    do_like_message(message=message, liker=current_user, to_id=message.from_id)
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
    logging.debug(f"Unliking message {message_id}")
    message.is_liked = False
    message.save()
    return Success(f"Unliked message {message_id}.")


@messages_bp.route("/messages/unseen", methods=["GET"])
@jwt_required
def get_new_messages():
    message_list = Message.get_multis(to_id=current_user.id, is_seen=False)
    new_messages = [m.to_dict() for m in message_list]
    logging.debug(f"Getting unseen messages for {current_user.id}")
    return SuccessOutput("new_messages", new_messages)
