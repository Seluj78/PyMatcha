import datetime
import json
import logging
from math import ceil

from PyMatcha import celery
from PyMatcha import redis
from PyMatcha.models.message import Message
from PyMatcha.models.user import User
from PyMatcha.utils.action_notifs.message import do_message
from PyMatcha.utils.bot_actions import _prepare_chatbot
from PyMatcha.utils.bot_actions import decide_bot_action
from PyMatcha.utils.recommendations import create_user_recommendations

BASE_HEAT_SCORE = 30
LIKES_MULTIPLIER = 2
SUPERLIKES_MULTIPLIER = 10
MATCHES_MULTIPLIER = 4
REPORTS_MULTIPLIER = 10
VIEW_MULTIPLIER = 1
MESSAGES_DIVIDER = 5
INACTIVITY_DIVIDER = 10


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, take_users_offline.s(), name="Update online users every minute")
    sender.add_periodic_task(3600, update_heat_scores.s(), name="Update heat scores every hour")
    sender.add_periodic_task(60, update_user_recommendations.s(), name="Update user recommendations every minute")
    sender.add_periodic_task(60, reset_superlikes.s(), name="Update user recommendations every minute")
    sender.add_periodic_task(30, take_random_users_online.s(), name="Set 250 random users online every 30 seconds")
    sender.add_periodic_task(
        600, calc_search_min_max.s(), name="Update Minimum and Maximum scores and ages for search every 10 minutes"
    )
    sender.add_periodic_task(180, random_bot_action.s(), name="Bots will do random actions")


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

        now = datetime.datetime.utcnow()
        monday1 = now - datetime.timedelta(days=now.weekday())
        monday2 = user.dt_lastseen - datetime.timedelta(days=user.dt_lastseen.weekday())
        weeks_passed_since_last_activity = int((monday1 - monday2).days / 7)

        score -= weeks_passed_since_last_activity * INACTIVITY_DIVIDER

        if score < 0:
            score = 0
        user.heat_score = score
        logging.debug(f"Setting score of {score} for user {user.id}")
        user.save()
    return "Successfully updated heat scores."


@celery.task
def take_users_offline():
    went_offline_count = 0
    stayed_online_count = 0
    for user in User.get_multis(is_online=True):
        if user.dt_lastseen + datetime.timedelta(minutes=2) < datetime.datetime.utcnow():
            user.is_online = False
            user.save()
            went_offline_count += 1
        else:
            stayed_online_count += 1
    logging.debug(f"{stayed_online_count} stayed online and {went_offline_count} went offline.")
    return f"{stayed_online_count} stayed online and {went_offline_count} went offline."


@celery.task
def update_user_recommendations():
    count = 0
    for user_to_update in User.get_multis(is_bot=False):
        create_user_recommendations(user_to_update)
        count += 1
    logging.debug(f"Successfully updated recommendations for {count} users.")
    return f"Successfully updated recommendations for {count} users."


@celery.task
def reset_superlikes():
    count = 0
    for user in User.select_all():
        if user.superlikes_counter <= 0 and user.superlikes_reset_dt <= datetime.datetime.utcnow():
            user.superlikes_counter = 5
            user.superlikes_reset_dt = None
            user.save()
            count += 1
    logging.debug(f"Reset superlikes for {count} users")
    return f"Reset superlikes for {count} users"


@celery.task
def calc_search_min_max():
    min_score = 9999
    max_score = 0
    min_age = 100
    max_age = 0
    for user in User.select_all():
        if not user.birthdate:
            continue
        if user.heat_score > max_score:
            max_score = user.heat_score
        if user.heat_score < min_score:
            min_score = user.heat_score

        today = datetime.datetime.utcnow()

        age = today.year - user.birthdate.year - ((today.month, today.day) < (user.birthdate.month, user.birthdate.day))

        if age > max_age:
            max_age = age
        if age < min_age:
            min_age = age
    minmax = {"min_score": min_score, "max_score": max_score, "min_age": min_age, "max_age": max_age}
    redis.set("search_minmax", json.dumps(minmax))
    return "Successfully updated min and max ages and scores"


@celery.task
def take_random_users_online():
    for user in User.select_random(250):
        if not user.is_bot:
            # User isn't a bot, so skip him
            continue
        user.is_online = True
        user.dt_lastseen = datetime.datetime.utcnow()
        user.save()
    return "Successfully set 250 users online"


@celery.task
def random_bot_action():
    for user in User.select_random_multis(1, is_bot=True, is_online=True):
        decide_bot_action(user)
    return "A bot has done actions"


@celery.task
def bot_respond_to_message(bot_id: int, from_id: int, message_content: str):
    bot_user = User.get(id=bot_id)
    from_user = User.get(id=from_id)

    chatbot = _prepare_chatbot(bot_user.username)
    reply = chatbot.get_response(message_content)
    do_message(from_user=bot_user, to_user=from_user, content=reply.text)

    logging.debug(f"Bot {bot_id} successfully replied to {from_id}")
    return f"Bot {bot_id} successfully replied to {from_id}"
