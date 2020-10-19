from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


if __name__ == "__main__":
    chatbot = ChatBot(
        "Training example",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri="sqlite:///database.sqlite3",
    )

    trainer = ChatterBotCorpusTrainer(chatbot)

    trainer.train("chatterbot.corpus.english")

    # ubuntu_trainer = UbuntuCorpusTrainer(chatbot)
    # ubuntu_trainer.train()

    while True:
        user_input = input("> ")
        print(chatbot.get_response(user_input), flush=True)
