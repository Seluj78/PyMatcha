import logging
import datetime

from PyMatcha import celery, redis

import PyMatcha.models.user as user_module

User = user_module.User


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, purge_offline_users.s(), name="Purge offline users every minute")


# TODO: array of id and one DB call
@celery.task
def purge_offline_users():
    logging.debug("Purging offline users")
    login_deadline_timestamp = float(datetime.datetime.utcnow().timestamp()) - 120
    count = 0
    for key in redis.scan_iter("user:*"):
        user_id = str(key).split(":")[1]
        date_lastseen = float(redis.get(key))
        if date_lastseen < login_deadline_timestamp:
            # delete the key
            u = User.get(id=user_id)
            u.date_lastseen = datetime.datetime.fromtimestamp(date_lastseen)
            u.is_online = False
            u.save()
            redis.delete(key)
            count += 1
    logging.debug("Purged {} users".format(count))
    return "Purged {} users".format(count)
