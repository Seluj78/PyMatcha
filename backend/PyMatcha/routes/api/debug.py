import datetime

import flask_jwt_extended as fjwt
import PyMatcha.models.user as user
from flask import Blueprint
from flask import current_app
from flask import jsonify
from PyMatcha import redis
from PyMatcha.errors import NotFoundError
from PyMatcha.models.view import View
from PyMatcha.success import Success
from PyMatcha.success import SuccessDeleted
from PyMatcha.utils.decorators import debug_token_required

debug_bp = Blueprint("debug", __name__)

User = user.User
get_user = user.get_user


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
        raise NotFoundError("User {} not found".format(uid), "Check the uid and try again")
    if u.is_confirmed:
        current_app.logger.debug("/debug/users/confirm -> User already confirmed")
        return Success("User already confirmed")
    u.is_confirmed = True
    u.confirmed_on = datetime.datetime.utcnow()
    u.save()
    current_app.logger.debug("/debug/users/confirm -> User {} confirmed.".format(u.id))
    return Success("User successfully confirmed")


@debug_bp.route("/debug/users/<uid>", methods=["DELETE"])
@debug_token_required
def delete_user(uid):
    current_app.logger.info("DELETE /debug/users/{} -> Call".format(uid))
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError("User {} not found".format(uid), "Check given id and try again")
    else:
        current_app.logger.info("/debug/users/{} -> DELETE user {}".format(uid, uid))
        u.delete()
        return SuccessDeleted("User {} Deleted".format(uid))


@debug_bp.route("/debug/views/<int:amount>", methods=["POST"])
@debug_token_required
@fjwt.jwt_required
def create_views(amount):
    current_user = fjwt.current_user
    for i in range(amount):
        View.create(profile_id=current_user.id, viewer_id=i)
    return Success(f"Added {amount} views to user {current_user.id}")


@debug_bp.route("/debug/views", methods=["DELETE"])
@debug_token_required
def delete_views():
    View.drop_table()
    View.create_table()
    return "", 204


@debug_bp.route("/debug/redis")
@debug_token_required
def debug_show_redis():
    ret = {"users": {}, "jtis": {}}
    for key in redis.scan_iter("user:*"):
        value = redis.get(str(key))
        ret["users"][key] = value
    for key in redis.scan_iter("jti:*"):
        value = redis.get(str(key))
        ret["jtis"][key] = value
    return jsonify(ret), 200
