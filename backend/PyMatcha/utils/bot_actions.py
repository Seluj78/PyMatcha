import json
import logging
from random import choice

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from PyMatcha import redis
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.message import Message
from PyMatcha.models.user import User
from PyMatcha.models.view import View
from PyMatcha.utils.recommendations import create_user_recommendations
from PyMatcha.utils.static import BACKEND_ROOT
from PyMatcha.utils.static import BOT_CONV_OPENERS


# TODO: DO superlikes


def _bot_response(bot_name, user_input):
    logging.debug(f"Starting chatbot with name {bot_name}")
    chatbot = ChatBot(
        bot_name,
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{BACKEND_ROOT}/../chatbot_database.sqlite3",
    )

    trainer = ChatterBotCorpusTrainer(chatbot, show_training_progress=False)
    trainer.train(
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.emotion",
        "chatterbot.corpus.english.greetings",
        "chatterbot.corpus.english.humor",
        "PyMatcha.utils.dating",
    )
    return chatbot.get_response(user_input)


def _get_recommendations(bot_user: User):
    recommendations = redis.get(f"user_recommendations:{str(bot_user.id)}")
    if not recommendations:
        create_user_recommendations(bot_user)
        recommendations = redis.get(f"user_recommendations:{str(bot_user.id)}")
        if not recommendations:
            raise ValueError("Recommendations could not be calculated")
    return json.loads(recommendations)


def botaction_like(bot_user: User):
    recommendations = _get_recommendations(bot_user)
    liked_ids = [like.liked_id for like in bot_user.get_likes_sent()]
    for user in recommendations:
        if user["id"] in liked_ids:
            recommendations.remove(user)
    try:
        user_to_like = choice(recommendations)
    except IndexError:
        return
    user_to_like = User.get(id=user_to_like["id"])
    View.create(profile_id=user_to_like.id, viewer_id=bot_user.id)
    Like.create(liker_id=bot_user.id, liked_id=user_to_like.id)

    if user_to_like.already_likes(bot_user.id):
        Match.create(user_1=bot_user.id, user_2=user_to_like.id)


def botaction_unlike(bot_user: User):
    liked_ids = [like.liked_id for like in bot_user.get_likes_sent()]
    try:
        id_to_unlike = choice(liked_ids)
    except IndexError:
        return
    Like.get_multi(liker_id=bot_user.id, liked_id=id_to_unlike).delete()


def botaction_view(bot_user: User):
    recommendations = _get_recommendations(bot_user)
    try:
        user_to_view = choice(recommendations)
    except IndexError:
        return
    View.create(profile_id=user_to_view["id"], viewer_id=bot_user.id)


def botaction_message_new_conversation(bot_user: User):
    matches = bot_user.get_matches()
    unopened_matches = []
    for match in matches:
        msg_1 = Message.get_multi(from_id=match.user_1, to_id=match.user_2)
        msg_2 = Message.get_multi(from_id=match.user_2, to_id=match.user_1)
        if not msg_1 and not msg_2:
            unopened_matches.append(match)

    try:
        match_to_open_conv = choice(unopened_matches)
    except IndexError:
        return

    if match_to_open_conv.user_1 == bot_user.id:
        other_user = match_to_open_conv.user_2
    else:
        other_user = match_to_open_conv.user_1

    bot_user.send_message(to_id=other_user, content=choice(BOT_CONV_OPENERS))


def botaction_respond_to_unread(bot_user: User):
    last_message_list = bot_user.get_conversation_list()

    unread_last_messages = []
    for last_message in last_message_list:
        if not last_message.is_seen and last_message.to_id == bot_user.id:
            unread_last_messages.append(last_message)
    try:
        message_to_reply = choice(unread_last_messages)
    except IndexError:
        return
    bot_reply = _bot_response(bot_user.username, message_to_reply.content)
    bot_user.send_message(to_id=message_to_reply.from_id, content=bot_reply)


def botaction_send_message_over_old_one(bot_user: User):
    last_message_list = bot_user.get_conversation_list()
    try:
        message_to_reply = choice(last_message_list)
    except IndexError:
        return
    if message_to_reply.to_id == bot_user.id:
        other_user = message_to_reply.from_id
    else:
        other_user = message_to_reply.to_id

    bot_reply = _bot_response(bot_user.username, ".")
    bot_user.send_message(to_id=other_user, content=bot_reply)
