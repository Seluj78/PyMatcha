import datetime
import json

from PyMatcha import redis
from PyMatcha.utils.match_score import _get_age_diff
from PyMatcha.utils.match_score import _get_common_tags
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.match_score import _get_gender_query


def default_date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def create_user_recommendations(user_to_update):
    today = datetime.datetime.utcnow()
    user_to_update_recommendations = []
    if not user_to_update.birthdate:
        return
    if not user_to_update.geohash:
        return

    user_to_update_age = (
        today.year
        - user_to_update.birthdate.year
        - ((today.month, today.day) < (user_to_update.birthdate.month, user_to_update.birthdate.day))
    )
    user_to_update_tags = [t.name for t in user_to_update.get_tags()]

    query = _get_gender_query(user_to_update.orientation, user_to_update.gender)

    if not query:
        return

    matches_id = [match.id for match in user_to_update.get_matches()]
    likes_sent_user_ids = [like.liked_id for like in user_to_update.get_likes_sent()]

    for user in query:
        if user.id == user_to_update.id:
            continue
        if user.id in matches_id or user.id in likes_sent_user_ids:
            continue
        score = 0

        distance = _get_distance(user_to_update.geohash, user.geohash)
        if distance:
            score -= distance

        user_age = (
            today.year - user.birthdate.year - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))
        )
        age_diff = _get_age_diff(user_to_update_age, user_age)
        score -= age_diff

        user_tags = [t.name for t in user.get_tags()]
        common_tags = _get_common_tags(user_to_update_tags, user_tags)
        score += len(common_tags) * 2

        score += user.heat_score

        d = {"score": score, "common_tags": common_tags, "distance": distance}
        d.update(user.to_dict())
        user_to_update_recommendations.append(d)
    user_to_update_recommendations_sorted = sorted(
        user_to_update_recommendations, key=lambda x: x["score"], reverse=True
    )
    redis.set(
        f"user_recommendations:{str(user_to_update.id)}",
        json.dumps(user_to_update_recommendations_sorted, default=default_date_converter),
    )
    redis.expire(f"user_recommendations:{str(user_to_update.id)}", 3600)
