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
from PyMatcha.utils.match_score import _get_inverted_gender


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, update_offline_users.s(), name="Update online users every minute")
    sender.add_periodic_task(3600, update_heat_scores.s(), name="Update heat scores every hour")


@celery.task
def update_heat_scores():
    for user in User.select_all():
        likes_received = len(user.get_likes_received())
        reports_received = len(user.get_reports_received())
        views = len(user.get_views())
        matches = len(user.get_matches())
        messages = len(Message.get_multi(to_id=user.id))

        score = 30
        if user.username == "seluj78" or user.username == "tet":
            score += 100
        score += likes_received * 2
        score += matches * 4
        # TODO: Superlike received = 5 pts
        score -= reports_received * 10
        score += views
        score += ceil(messages / 5)
        # TODO: remove 10 pts per week of inactivity
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
    for key in redis.scan_iter("user:*"):
        # Get the user id
        user_id = str(key).split(":")[1]
        date_lastseen = float(redis.get(key))
        # If the user has passed the deadline
        if date_lastseen < login_deadline_timestamp:
            try:
                u = User.get(id=user_id)
            except ValueError:
                # Edge case where the user has been deleted from DB while he was still online
                pass
            else:
                # TODO: array of id and one DB call to update the db as offline
                u.date_lastseen = datetime.datetime.fromtimestamp(date_lastseen)
                u.is_online = False
                u.save()
                offline_count += 1
            # delete the key in redis, setting the user as offline in redis
            redis.delete(key)
            count += 1
        else:
            try:
                u = User.get(id=user_id)
            except ValueError:
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
