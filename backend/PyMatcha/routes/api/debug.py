import datetime

from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha import redis
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.message import Message
from PyMatcha.models.report import Report
from PyMatcha.models.tag import Tag
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.models.view import View
from PyMatcha.utils.decorators import debug_token_required
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.populate_database import populate_users
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessDeleted
from PyMatcha.utils.tasks import update_user_recommendations

debug_bp = Blueprint("debug", __name__)


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


@debug_bp.route("/debug/users/<uid>", methods=["DELETE"])
@debug_token_required
def delete_user(uid):
    current_app.logger.info("DELETE /debug/users/{} -> Call".format(uid))
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError("User {} not found".format(uid))
    else:
        current_app.logger.info("/debug/users/{} -> DELETE user {}".format(uid, uid))
        u.delete()
        return SuccessDeleted("User {} Deleted.".format(uid))


@debug_bp.route("/debug/views/<int:amount>", methods=["POST"])
@debug_token_required
@jwt_required
def create_views(amount):
    for i in range(amount):
        View.create(profile_id=current_user.id, viewer_id=i)
    return Success(f"Added {amount} views to user {current_user.id}.")


@debug_bp.route("/debug/redis")
@debug_token_required
def debug_show_redis():
    ret = dict()
    for key in redis.scan_iter("*"):
        ret[key] = redis.get(str(key))
    return jsonify(ret), 200


@debug_bp.route("/debug/reports", methods=["GET"])
@debug_token_required
def debug_get_all_reports():
    report_list = []
    for r in Report.select_all():
        report_list.append(r.to_dict())
    return jsonify(report_list)


@debug_bp.route("/debug/reports/<uid>", methods=["GET"])
@debug_token_required
def debug_get_user_reports(uid):
    u = get_user(uid)
    reports_received = [r.to_dict() for r in u.get_reports_received()]
    reports_sent = [r.to_dict() for r in u.get_reports_sent()]
    return jsonify({"reports_received": reports_received, "reports_sent": reports_sent}), 200


DEBUG_CREATE_FAKE_REPORT = {"reporter_id": int, "reported_id": int, "reason": str, "details": str}


@debug_bp.route("/debug/reports", methods=["POST"])
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


DEBUG_CREATE_FAKE_LIKE = {"liker_uid": str, "liked_uid": str}


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


@debug_bp.route("/debug/tables", methods=["DELETE"])
@debug_token_required
def delete_tables():
    Match.drop_table()
    Like.drop_table()
    Report.drop_table()
    View.drop_table()
    User.drop_table()
    Tag.drop_table()
    Message.drop_table()

    Match.create_table()
    Like.create_table()
    Report.create_table()
    View.create_table()
    User.create_table()
    Tag.create_table()
    Message.create_table()
    return "", 204


@debug_bp.route("/debug/redis", methods=["DELETE"])
@debug_token_required
def delete_redis():
    redis.flushdb()
    return "", 204


DEBUG_SEND_MESSAGE = {"from_uid": str, "to_uid": str, "content": str}


@debug_bp.route("/debug/messages/send", methods=["POST"])
@debug_token_required
@validate_params(DEBUG_SEND_MESSAGE)
def debug_send_message():
    data = request.get_json()
    from_id = get_user(data["from_uid"]).id
    to_id = get_user(data["to_uid"]).id
    Message.create(from_id=from_id, to_id=to_id, content=data["content"])
    return "", 204


@debug_bp.route("/debug/recommendations/start", methods=["POST"])
@debug_token_required
def debug_recommendations_start_process():
    """This function will create 100 random users and calculate recommendations"""
    populate_users(amount=100, drop_user_table=False)
    update_user_recommendations()
    return Success("Done")
