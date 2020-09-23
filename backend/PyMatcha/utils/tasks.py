import datetime
import json
import logging
from math import ceil

from PyMatcha import celery
from PyMatcha import redis
from PyMatcha.models.message import Message
from PyMatcha.models.user import User
from PyMatcha.utils.match_score import _get_age_diff
from PyMatcha.utils.match_score import _get_common_tags
from PyMatcha.utils.match_score import _get_distance
from PyMatcha.utils.match_score import _get_gender_query

BASE_HEAT_SCORE = 30
LIKES_MULTIPLIER = 2
SUPERLIKES_MULTIPLIER = 10
MATCHES_MULTIPLIER = 4
REPORTS_MULTIPLIER = 10
VIEW_MULTIPLIER = 1
MESSAGES_DIVIDER = 5


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, update_offline_users.s(), name="Update online users every minute")
    sender.add_periodic_task(3600, update_heat_scores.s(), name="Update heat scores every hour")
    sender.add_periodic_task(60, update_user_recommendations.s(), name="Update user recommendations every minute")


@celery.task
def update_heat_scores():
    for user in User.select_all():
        likes = [like.is_superlike for like in user.get_likes_received()]
        likes_received = likes.count(False)
        superlikes_received = likes.count(True)
        reports_received = len(user.get_reports_received())
        views = len(user.get_views())
        matches = len(user.get_matches())
        messages = Message.get_multi(to_id=user.id)
        if not messages:
            messages = 0
        else:
            messages = len(messages)

        score = BASE_HEAT_SCORE
        if user.username == "seluj78" or user.username == "lauris":
            score += 100
        score += likes_received * LIKES_MULTIPLIER
        score += superlikes_received * SUPERLIKES_MULTIPLIER
        score += matches * MATCHES_MULTIPLIER
        score -= reports_received * REPORTS_MULTIPLIER
        score += views * VIEW_MULTIPLIER
        score += ceil(messages / MESSAGES_DIVIDER)
        user.heat_score = score
        user.save()
        return f"Updated heat score for user {user.id}: {user.heat_score}."


@celery.task
def update_offline_users():
    logging.debug("Updating offline users")
    # Get the last login deadline
    login_deadline_timestamp = float(datetime.datetime.utcnow().timestamp()) - 120
    count = 0
    online_count = 0
    offline_count = 0
    # For all user keys
    for key in redis.scan_iter("online_user:*"):
        # Get the user id
        user_id = str(key).split(":")[1]
        date_lastseen = float(redis.get(key))
        # If the user has passed the deadline
        if date_lastseen < login_deadline_timestamp:
            u = User.get(id=user_id)
            if u:
                u.date_lastseen = datetime.datetime.fromtimestamp(date_lastseen)
                u.is_online = False
                u.save()
                offline_count += 1
            # delete the key in redis, setting the user as offline in redis
            redis.delete(key)
            count += 1
        else:
            u = User.get(id=user_id)
            if not u:
                # Edge case where the user has been deleted from DB while he was still online
                redis.delete(key)
            else:
                u.date_lastseen = datetime.datetime.fromtimestamp(date_lastseen)
                u.is_online = True
                u.save()
                online_count += 1
            count += 1
    logging.debug(
        "Updated online status for {} users. {} passed offline and {} passed or stayed online.".format(
            count, offline_count, online_count
        )
    )
    return "Updated online status for {} users. {} passed offline and {} passed or stayed online.".format(
        count, offline_count, online_count
    )


def default_date_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@celery.task
def update_user_recommendations():
    today = datetime.datetime.utcnow()
    count = 0
    for user_to_update in User.select_all():
        count += 1
        user_to_update_recommendations = []
        if not user_to_update.birthdate:
            continue
        if not user_to_update.geohash:
            continue

        user_to_update_age = (
            today.year
            - user_to_update.birthdate.year
            - ((today.month, today.day) < (user_to_update.birthdate.month, user_to_update.birthdate.day))
        )
        user_to_update_tags = [t.name for t in user_to_update.get_tags()]

        query = _get_gender_query(user_to_update.orientation, user_to_update.gender)

        for user in query:
            if user.id == user_to_update.id:
                continue
            score = 0

            distance = _get_distance(user_to_update.geohash, user.geohash)
            if distance:
                score -= distance

            user_age = (
                today.year
                - user.birthdate.year
                - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))
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
    return f"Successfully updated recommendations for {count} users."


@celery.task
def set_user_superlikes(user_id, amount=5):
    redis.set(f"superlikes:{user_id}", amount)
