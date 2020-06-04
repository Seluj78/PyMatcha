import datetime
import logging

from PyMatcha import celery
from PyMatcha import redis
from PyMatcha.models.user import User


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, update_offline_users.s(), name="Update online users every minute")


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
        "Updated online status for {} users. {} passed offline and {} passed or stayed online".format(
            count, offline_count, online_count
        )
    )
    return "Updated online status for {} users. {} passed offline and {} passed or stayed online".format(
        count, offline_count, online_count
    )
