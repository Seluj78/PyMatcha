from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.notification import Notification
from PyMatcha.models.user import get_user
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success

like_bp = Blueprint("like", __name__)


@like_bp.route("/like/<uid>", methods=["POST"])
@validate_params({"is_superlike": bool})
@jwt_required
def like_profile(uid):

    is_superlike = request.get_json()["is_superlike"]

    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == u.id:
        raise BadRequestError("Cannot like yourself.")
    if current_user.already_likes(u.id):
        raise BadRequestError("You already liked this person.")

    if is_superlike:
        if current_user.superlikes_counter <= 0:
            if current_user.superlikes_reset_dt < datetime.utcnow():
                raise BadRequestError("Your superlikes are being restored, try again in a second")
            else:
                next_reset_delta = current_user.superlikes_reset_dt - datetime.utcnow()
                seconds = next_reset_delta.total_seconds()
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = int(seconds % 60)
                raise BadRequestError(f"No more superlikes today, come back in {hours}h:{minutes}m:{seconds}s")
        else:
            current_user.superlikes_counter -= 1
            if current_user.superlikes_counter <= 0:
                current_user.superlikes_reset_dt = datetime.utcnow() + timedelta(hours=12)
            current_user.save()

    Like.create(liker_id=current_user.id, liked_id=u.id, is_superlike=is_superlike)

    if u.already_likes(current_user.id):
        Match.create(user_1=current_user.id, user_2=u.id)
        Notification.create(
            trigger_id=current_user.id,
            user_id=u.id,
            content=f"{current_user.first_name} liked you! Go check them out!",
            type="like",
            link_to=f"users/{current_user.id}",
        )
        Notification.create(
            trigger_id=current_user.id,
            user_id=u.id,
            content=f"You and {current_user.first_name} matched!",
            type="match",
            link_to=f"conversation/{current_user.id}",
        )
        Notification.create(
            trigger_id=u.id,
            user_id=current_user.id,
            content=f"You and {u.first_name} matched!",
            type="match",
            link_to=f"conversation/{u.id}",
        )
        return Success("It's a match !")

    if is_superlike:
        Notification.create(
            trigger_id=current_user.id,
            user_id=u.id,
            content=f"{current_user.first_name} superliked you 😏! Go check them out!",
            type="superlike",
            link_to=f"users/{current_user.id}",
        )
        return Success("Superliked user.")
    else:
        Notification.create(
            trigger_id=current_user.id,
            user_id=u.id,
            content=f"{current_user.first_name} liked you! Go check them out!",
            type="like",
            link_to=f"users/{current_user.id}",
        )
        return Success("Liked user.")


@like_bp.route("/unlike/<uid>", methods=["POST"])
@jwt_required
def unlike_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == u.id:
        raise BadRequestError("Cannot unlike yourself.")
    if not current_user.already_likes(u.id):
        raise BadRequestError("You never liked this person in the first place.")
    Like.get_multi(liked_id=u.id, liker_id=current_user.id).delete()

    m1 = Match.get_multi(user_1=u.id, user_2=current_user.id)
    m2 = Match.get_multi(user_1=current_user.id, user_2=u.id)

    if m1:
        m1.delete()
    elif m2:
        m2.delete()

    Notification.create(
        trigger_id=current_user.id,
        user_id=u.id,
        content=f"{current_user.first_name} unliked you.",
        type="unlike",
        link_to=None,
    )

    return Success(f"Unliked user {u.id}.")
