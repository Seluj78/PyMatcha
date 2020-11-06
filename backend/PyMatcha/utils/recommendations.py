import datetime
import json
import logging

from PyMatcha import redis
from PyMatcha.models.user import User
from PyMatcha.utils.match_score import _get_age_diff
from PyMatcha.utils.match_score import _get_common_tags
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.match_score import _get_gender_query


def default_date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def create_user_recommendations(user_to_update: User, ignore_bots: bool = False):
    logging.debug(f"Creating recommendations for user {user_to_update.id}")
    today = datetime.datetime.utcnow()
    user_to_update_recommendations = []
    if not user_to_update.birthdate:
        logging.warning(f"Cannot create recommendations for user {user_to_update.id}: Missing birthdate")
        return
    if not user_to_update.geohash:
        logging.warning(f"Cannot create recommendations for user {user_to_update.id}: Missing geohash")
        return

    user_to_update_age = (
        today.year
        - user_to_update.birthdate.year
        - ((today.month, today.day) < (user_to_update.birthdate.month, user_to_update.birthdate.day))
    )
    user_to_update_tags = [t.name for t in user_to_update.get_tags()]

    logging.debug(f"Getting gender query for recommendations of user {user_to_update.id}")
    query = _get_gender_query(user_to_update.orientation, user_to_update.gender)

    if not query:
        return

    matches_id = [match.id for match in user_to_update.get_matches()]
    likes_sent_user_ids = [like.liked_id for like in user_to_update.get_likes_sent()]
    blocked_ids = [u.blocked_id for u in user_to_update.get_blocks()]

    for user in query:
        if user.is_bot and ignore_bots:
            logging.debug(
                f"Recommendations for user {user_to_update.id}: Ignoring user {user.id} because "
                f"it's a bot and `ignore_bot` is set"
            )
            continue
        if user.id == user_to_update.id:
            logging.debug(f"Recommendations for user {user_to_update.id}: Ignoring user {user.id} it's the same person")
            continue
        if user.id in matches_id or user.id in likes_sent_user_ids:
            logging.debug(
                f"Recommendations for user {user_to_update.id}: Ignoring user {user.id} because "
                f"already liked or matched"
            )
            continue
        if user.id in blocked_ids:
            logging.debug(f"Recommendations for user {user_to_update.id}: Ignoring user {user.id} because blocked")
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
    logging.debug(f"Recommendations for user {user_to_update.id}: Setting recommendations to redis")
    redis.set(
        f"user_recommendations:{str(user_to_update.id)}",
        json.dumps(user_to_update_recommendations_sorted, default=default_date_converter),
    )
    logging.debug(f"Recommendations for user {user_to_update.id}: Setting expiry to redis")
    redis.expire(f"user_recommendations:{str(user_to_update.id)}", 3600)
