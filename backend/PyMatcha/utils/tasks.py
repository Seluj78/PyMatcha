import datetime
import logging
from math import ceil

from PyMatcha import celery
from PyMatcha import redis
from PyMatcha.models.message import Message
from PyMatcha.models.user import User
from PyMatcha.utils.recommendations import create_user_recommendations

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
        if score < 0:
            score = 0
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


@celery.task
def update_user_recommendations():
    count = 0
    for user_to_update in User.select_all():
        create_user_recommendations(user_to_update)
    return f"Successfully updated recommendations for {count} users."


@celery.task
def set_user_superlikes(user_id, amount=5):
    redis.set(f"superlikes:{user_id}", amount)
