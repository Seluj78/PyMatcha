from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.user import User
from PyMatcha.utils.match_score import _get_common_tags
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.success import SuccessOutput


history_bp = Blueprint("history_bp", __name__)


@history_bp.route("/history/viewed")
@jwt_required
def history_viewed_people():
    views = current_user.get_view_history()
    viewed_people = []
    for view in views:
        user = User.get(id=view.profile_id)
        distance = _get_distance(current_user.geohash, user.geohash)
        user_tags = [t.name for t in user.get_tags()]
        current_user_tags = [t.name for t in current_user.get_tags()]
        common_tags = _get_common_tags(current_user_tags, user_tags)
        user_dict = user.to_dict()
        user_dict["common_tags"] = common_tags
        user_dict["distance"] = distance
        viewed_people.append(user_dict)
    return SuccessOutput("viewed", viewed_people)


@history_bp.route("/history/viewed/me", methods=["GET"])
@jwt_required
def history_viewed_me():
    views = current_user.get_views()
    viewed_people = []
    for view in views:
        user = User.get(id=view.viewer_id)
        distance = _get_distance(current_user.geohash, user.geohash)
        user_tags = [t.name for t in user.get_tags()]
        current_user_tags = [t.name for t in current_user.get_tags()]
        common_tags = _get_common_tags(current_user_tags, user_tags)
        user_dict = user.to_dict()
        user_dict["common_tags"] = common_tags
        user_dict["distance"] = distance
        viewed_people.append(user_dict)
    return SuccessOutput("viewed_me", viewed_people)


@history_bp.route("/history/liked", methods=["GET"])
@jwt_required
def history_liked_people():
    likes = current_user.get_likes_sent()
    liked_people = []
    for like in likes:
        user = User.get(id=like.liked_id)
        distance = _get_distance(current_user.geohash, user.geohash)
        user_tags = [t.name for t in user.get_tags()]
        current_user_tags = [t.name for t in current_user.get_tags()]
        common_tags = _get_common_tags(current_user_tags, user_tags)
        user_dict = user.to_dict()
        user_dict["common_tags"] = common_tags
        user_dict["distance"] = distance
        liked_people.append(user_dict)
    return SuccessOutput("liked", liked_people)


@history_bp.route("/history/liked/me", methods=["GET"])
@jwt_required
def history_liked_me():
    likes = current_user.get_likes_received()
    liked_people = []
    for like in likes:
        user = User.get(id=like.liker_id)
        distance = _get_distance(current_user.geohash, user.geohash)
        user_tags = [t.name for t in user.get_tags()]
        current_user_tags = [t.name for t in current_user.get_tags()]
        common_tags = _get_common_tags(current_user_tags, user_tags)
        user_dict = user.to_dict()
        user_dict["common_tags"] = common_tags
        user_dict["distance"] = distance
        liked_people.append(user_dict)
    return SuccessOutput("liked_me", liked_people)


@history_bp.route("/history/blocked", methods=["GET"])
@jwt_required
def history_blocked():
    blocks = current_user.get_blocks()
    blocked_people = []
    for block in blocks:
        user = User.get(id=block.blocked_id)
        distance = _get_distance(current_user.geohash, user.geohash)
        user_tags = [t.name for t in user.get_tags()]
        current_user_tags = [t.name for t in current_user.get_tags()]
        common_tags = _get_common_tags(current_user_tags, user_tags)
        user_dict = user.to_dict()
        user_dict["common_tags"] = common_tags
        user_dict["distance"] = distance
        blocked_people.append(user_dict)
    return SuccessOutput("liked_me", blocked_people)
