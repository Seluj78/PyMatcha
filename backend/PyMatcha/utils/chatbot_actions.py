import logging

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from PyMatcha.utils.static import BACKEND_ROOT


def get_chatbot_response(bot_name, user_input):
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
