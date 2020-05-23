import datetime
import logging

import PyMatcha.models.user as user_module
from PyMatcha import celery
from PyMatcha import redis

User = user_module.User


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, purge_offline_users.s(), name="Purge offline users every minute")


@celery.task
def purge_offline_users():
    logging.debug("Purging offline users")
    # Get the last login deadline
    login_deadline_timestamp = float(datetime.datetime.utcnow().timestamp()) - 120
    count = 0
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
            # delete the key in redis, setting the user as offline in redis
            redis.delete(key)
            count += 1
    logging.debug("Purged {} users".format(count))
    return "Purged {} users".format(count)
