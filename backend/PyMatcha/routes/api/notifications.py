from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.notification import Notification
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications", methods=["GET"])
@jwt_required
def get_all_notifications():
    return SuccessOutput("notifications", current_user.get_all_notifications())


@notifications_bp.route("/notifications/unread", methods=["GET"])
@jwt_required
def get_unread_notifications():
    return SuccessOutput("notifications", current_user.get_unread_notifications())


@notifications_bp.route("/notifications/read/<n_id>", methods=["POST"])
@jwt_required
def mark_notification_as_read(n_id):
    notif = Notification.get(id=n_id)
    if not notif:
        raise NotFoundError(f"Notification id {n_id} not found.")
    if notif.user_id != current_user.id:
        raise BadRequestError("Cannot mark notification as read if it isn't yours.")
    notif.is_seen = True
    notif.save()
    return Success("Mark as read.")
