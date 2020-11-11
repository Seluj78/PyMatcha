import datetime
import json
import logging

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha import redis
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.match_score import _get_common_tags
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.match_score import _get_gender_query
from PyMatcha.utils.success import SuccessOutput
from PyMatcha.utils.tasks import calc_search_min_max

search_bp = Blueprint("search", __name__)

REQUIRED_PARAMS_SEARCH = {
    "min_age": int,
    "max_age": int,
    "min_score": int,
    "max_score": int,
    "tags": list,
    "max_distance": int,
}


@search_bp.route("/search", methods=["POST"])
@validate_params(REQUIRED_PARAMS_SEARCH, allow_empty=True)
@jwt_required
def search():
    data = request.get_json()
    min_age = int(data["min_age"])
    max_age = int(data["max_age"])
    min_score = int(data["min_score"])
    max_score = int(data["max_score"])
    max_distance = int(data["max_distance"])
    tags = data["tags"]
    logging.info(f"Running search for user {current_user.id} with params {data}")

    today = datetime.datetime.utcnow()

    query = _get_gender_query(current_user.orientation, current_user.gender)
    matches_id = [match.id for match in current_user.get_matches()]
    likes_sent_user_ids = [like.liked_id for like in current_user.get_likes_sent()]
    blocked_ids = [u.blocked_id for u in current_user.get_blocks()]
    returned_list = []
    for user in query:
        if user.id == current_user.id:
            continue
        if user.id in matches_id or user.id in likes_sent_user_ids:
            continue
        if user.id in blocked_ids:
            continue

        user_age = (
            today.year - user.birthdate.year - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))
        )

        if max_age != -1:
            if user_age >= max_age:
                continue
        if min_age != -1:
            if user_age <= min_age:
                continue

        if max_score != -1:
            if user.heat_score >= max_score:
                continue
        if min_score != -1:
            if user.heat_score <= min_score:
                continue

        distance = _get_distance(current_user.geohash, user.geohash)
        if distance:
            if distance >= max_distance:
                if max_distance != -1:
                    continue
        else:
            distance = -1
            if max_distance != -1:
                raise BadRequestError("user needs to sets his location first.")

        common_tags = []
        if tags:
            user_tags = [t.name for t in user.get_tags()]
            common_tags = _get_common_tags(tags, user_tags)
            if not common_tags:
                # No tags has been found
                continue

        user_dict = user.to_dict()
        user_dict["distance"] = distance
        user_dict["common_tags"] = common_tags
        returned_list.append(user_dict)
    return SuccessOutput("search_results", returned_list)


@search_bp.route("/search/values", methods=["GET"])
def get_min_maxes_values():
    try:
        minmax = json.loads(redis.get("search_minmax"))
    except TypeError:
        calc_search_min_max()
        minmax = json.loads(redis.get("search_minmax"))
    logging.info(f"Returning min and max search values {minmax}")
    return SuccessOutput("search_minmax", minmax)
