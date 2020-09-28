import datetime

from flask import Blueprint
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.match_score import _get_common_tags
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.match_score import _get_gender_query
from PyMatcha.utils.success import SuccessOutput

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

    today = datetime.datetime.utcnow()

    query = _get_gender_query(current_user.orientation, current_user.gender)
    returned_list = []
    for user in query:
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
            raise BadRequestError("user needs to sets his location first")

        user_tags = [t.name for t in user.get_tags()]
        common_tags = _get_common_tags(tags, user_tags)
        if not common_tags:
            if tags:
                continue

        user_dict = user.to_dict()
        user_dict.update({"distance": distance, "common_tags": common_tags})
        returned_list.append(user_dict)
    return SuccessOutput("search_results", returned_list)
