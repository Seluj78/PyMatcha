import json
import logging
from random import choice

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from PyMatcha import redis
from PyMatcha.models.like import Like
from PyMatcha.models.user import User
from PyMatcha.models.view import View
from PyMatcha.utils.recommendations import create_user_recommendations
from PyMatcha.utils.static import BACKEND_ROOT

# TODO: message new conversation, respond to unread message, send a new message in already started conversation


def bot_response(bot_name, user_input):
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


def bot_like(bot_user: User, is_superlike: bool):
    recommendations = _get_recommendations(bot_user)
    liked_ids = [like.liked_id for like in bot_user.get_likes_sent()]
    for user in recommendations:
        if user["id"] in liked_ids:
            recommendations.remove(user)
    user_to_like = choice(recommendations)
    Like.create(liker_id=bot_user.id, liked_id=user_to_like["id"], is_superlike=is_superlike)


def bot_unlike(bot_user: User):
    liked_ids = [like.liked_id for like in bot_user.get_likes_sent()]
    id_to_unlike = choice(liked_ids)
    Like.get_multi(liker_id=bot_user.id, liked_id=id_to_unlike).delete()


def bot_view(bot_user: User):
    recommendations = _get_recommendations(bot_user)
    user_to_view = choice(recommendations)
    View.create(profile_id=user_to_view["id"], viewer_id=bot_user.id)
