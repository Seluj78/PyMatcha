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
    current_timestamp = int(datetime.datetime.utcnow().timestamp()) + 120
    for key in redis.scan_iter("user:*"):
        user_id = str(key).split(":")[1]
        date_lastseen = int(redis.get(user_id))
        if date_lastseen < current_timestamp:
            # delete the key
            u = User.get(id=id)
            u.is_online = False
            u.save()
            redis.delete(key)
