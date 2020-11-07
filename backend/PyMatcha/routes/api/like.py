from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.user import get_user
from PyMatcha.utils.action_notifs.like import do_like
from PyMatcha.utils.action_notifs.like import do_match
from PyMatcha.utils.action_notifs.like import do_superlike
from PyMatcha.utils.action_notifs.like import do_unlike
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from timeago import format as timeago_format

like_bp = Blueprint("like", __name__)


@like_bp.route("/like/<uid>", methods=["POST"])
@validate_params({"is_superlike": bool})
@jwt_required
def like_profile(uid):

    is_superlike = request.get_json()["is_superlike"]

    try:
        liked_user = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == liked_user.id:
        raise BadRequestError("Cannot like yourself.")
    if current_user.already_likes(liked_user.id):
        raise BadRequestError("You already liked this person.")

    if is_superlike:
        if current_user.superlikes_counter <= 0:
            if current_user.superlikes_reset_dt < datetime.utcnow():
                raise BadRequestError("Your superlikes are being restored, try again in a few seconds.")
            else:
                ta_format = timeago_format(current_user.superlikes_reset_dt, datetime.utcnow())
                raise BadRequestError(f"No more superlikes today, come back {ta_format}")
        else:
            current_user.superlikes_counter -= 1
            if current_user.superlikes_counter <= 0:
                current_user.superlikes_reset_dt = datetime.utcnow() + timedelta(hours=12)
            current_user.save()

    if is_superlike:
        do_superlike(liker_user=current_user, liked_user_id=liked_user.id)
    else:
        do_like(liker_user=current_user, liked_user_id=liked_user.id)

    if liked_user.already_likes(current_user.id):
        do_match(liker_user=current_user, liked_user=liked_user)
        return Success("It's a match !")

    if is_superlike:
        return Success("Superliked user.")
    else:
        return Success("Liked user.")


@like_bp.route("/unlike/<uid>", methods=["POST"])
@jwt_required
def unlike_profile(uid):
    try:
        unliked_user = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == unliked_user.id:
        raise BadRequestError("Cannot unlike yourself.")
    if not current_user.already_likes(unliked_user.id):
        raise BadRequestError("You never liked this person in the first place.")
    do_unlike(current_user, unliked_user.id)

    return Success("Unliked user.")
