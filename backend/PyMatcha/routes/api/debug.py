import datetime

import PyMatcha.models.user as user
from flask import Blueprint
from flask import current_app
from PyMatcha.errors import NotFoundError
from PyMatcha.success import Success
from PyMatcha.utils.decorators import debug_token_required

debug_bp = Blueprint("debug", __name__)

User = user.User
get_user = user.get_user


@debug_bp.route("/debug/users/confirm/<uid>", methods=["POST"])
@debug_token_required
def debug_confirm_user(uid):
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
