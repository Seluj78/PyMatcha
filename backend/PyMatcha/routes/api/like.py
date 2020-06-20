from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.user import get_user
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success

like_bp = Blueprint("like", __name__)


@like_bp.route("/like/<uid>", methods=["POST"])
@jwt_required
def like_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found", "try again")
    if current_user.id == u.id:
        raise BadRequestError("Cannot like yourself", "Try again")
    if current_user.already_likes(u.id):
        raise BadRequestError("You already liked this person", "Try again")
    Like.create(liker_id=current_user.id, liked_id=u.id)

    if current_user.already_likes(u.id):
        Match.create(user_1=current_user.id, user_2=u.id)
        return Success(f"Liked user {u.id}, it's a match !")

    return Success(f"Liked user {u.id}.")


@like_bp.route("/unlike/<uid>", methods=["POST"])
@jwt_required
def unlike_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found", "try again")
    if current_user.id == u.id:
        raise BadRequestError("Cannot unlike yourself", "Try again")
    if not current_user.already_likes(u.id):
        raise BadRequestError("You never liked this person in the first place", "Try again")
    Like.get_multi(liked_id=u.id, liker_id=current_user.id).delete()
    return Success(f"Unliked user {u.id}.")


# TODO: Likes received
# TODO: Likes sent
