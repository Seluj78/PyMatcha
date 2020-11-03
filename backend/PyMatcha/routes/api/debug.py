import datetime

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha import redis
from PyMatcha.models.like import Like
from PyMatcha.models.message import Message
from PyMatcha.models.notification import Notification
from PyMatcha.models.report import Report
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.models.view import View
from PyMatcha.utils.decorators import debug_token_required
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput


debug_bp = Blueprint("debug", __name__)

DEBUG_SEND_MESSAGE = {"from_uid": str, "to_uid": str, "content": str}
DEBUG_CREATE_FAKE_REPORT = {"reporter_id": int, "reported_id": int, "reason": str, "details": str}
DEBUG_CREATE_FAKE_LIKE = {"liker_uid": str, "liked_uid": str}


@debug_bp.route("/debug/users/confirm/<uid>", methods=["POST"])
@debug_token_required
def debug_confirm_user(uid):
    """
    This route confirms a given user without having to send and receive an email
    """
    current_app.logger.debug("/debug/users/confirm/{} -> Call".format(uid))
    try:
        u = get_user(uid)
    except NotFoundError:
        current_app.logger.debug("/debug/users/confirm -> User not found")
        raise NotFoundError("User {} not found".format(uid))
    if u.is_confirmed:
        current_app.logger.debug("/debug/users/confirm -> User already confirmed")
        return Success("User already confirmed.")
    u.is_confirmed = True
    u.confirmed_on = datetime.datetime.utcnow()
    u.save()
    current_app.logger.debug("/debug/users/confirm -> User {} confirmed.".format(u.id))
    return Success("User successfully confirmed.")


@debug_bp.route("/debug/views/<int:amount>", methods=["POST"])
@debug_token_required
@jwt_required
def create_views(amount):
    users = User.select_random(amount)
    for user in users:
        View.create(profile_id=current_user.id, viewer_id=user.id)
    return Success(f"Added {amount} views to user {current_user.id}.")


@debug_bp.route("/debug/redis")
@debug_token_required
def debug_show_redis():
    ret = dict()
    for key in redis.scan_iter("*"):
        ret[key] = redis.get(str(key))
    return jsonify(ret), 200


@debug_bp.route("/debug/report", methods=["POST"])
@debug_token_required
@validate_params(DEBUG_CREATE_FAKE_REPORT)
def debug_create_report():
    data = request.get_json()
    reporter_id = data["reporter_id"]
    reported_id = data["reported_id"]
    reason = data["reason"]
    details = data["details"]
    Report.create(reported_id=reported_id, reporter_id=reporter_id, reason=reason, details=details)
    return "", 204


@debug_bp.route("/debug/like", methods=["POST"])
@debug_token_required
@validate_params(DEBUG_CREATE_FAKE_LIKE)
def create_fake_like():
    data = request.get_json()
    liker_uid = data["liker_uid"]
    liked_uid = data["liked_uid"]
    liker = get_user(liker_uid)
    liked = get_user(liked_uid)

    Like.create(liker_id=liker.id, liked_id=liked.id)
    return "", 204


@debug_bp.route("/debug/superlikes_set/<uid>/<amount>", methods=["POST"])
@debug_token_required
def set_superlikes(uid, amount):
    user = User.get(id=uid)
    user.superlikes_counter = amount
    user.save()
    return "", 200


@debug_bp.route("/debug/messages/send", methods=["POST"])
@debug_token_required
@validate_params(DEBUG_SEND_MESSAGE)
def debug_send_message():
    data = request.get_json()
    from_id = get_user(data["from_uid"]).id
    to_id = get_user(data["to_uid"]).id
    Message.create(from_id=from_id, to_id=to_id, content=data["content"])
    return "", 200


@debug_bp.route("/debug/messages/<uid>", methods=["GET"])
@debug_token_required
def debug_get_user_messages(uid):
    user = get_user(uid)
    messages = [msg.to_dict() for msg in user.get_messages()]
    return SuccessOutput("messages", messages)


@debug_bp.route("/debug/reset/<uid>", methods=["DELETE"])
@debug_token_required
def debug_reset_ci(uid):
    user = get_user(uid)
    [entry.delete() for entry in user.get_tags()]
    [entry.delete() for entry in user.get_views()]
    [entry.delete() for entry in user.get_view_history()]
    [entry.delete() for entry in user.get_reports_received()]
    [entry.delete() for entry in user.get_reports_sent()]
    [entry.delete() for entry in user.get_messages()]
    [entry.delete() for entry in user.get_matches()]
    [entry.delete() for entry in user.get_likes_sent()]
    [entry.delete() for entry in user.get_likes_received()]
    [entry.delete() for entry in user.get_blocks()]
    [entry.delete() for entry in Notification.select_all()]
    user.delete()
    user = get_user(1500)
    [entry.delete() for entry in user.get_messages()]
    return "", 200
