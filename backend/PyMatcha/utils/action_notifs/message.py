import logging

from PyMatcha.models.message import Message
from PyMatcha.models.notification import Notification
from PyMatcha.models.user import User


def do_message(from_user: User, to_user: User, content: str):
    logging.info(f"{from_user.id} messaged {to_user.id}")
    from_user.send_message(to_id=to_user.id, content=content)
    Notification.create(
        trigger_id=from_user.id,
        user_id=to_user.id,
        content=f"{from_user.first_name} said: {content}",
        type="message",
        link_to=f"conversation/{from_user.id}",
    )


def do_like_message(message: Message, liker: User, to_id: int):
    logging.debug(f"{liker.id} liked message {message.id} of user {to_id}")
    message.is_liked = True
    message.save()
    Notification.create(
        trigger_id=liker.id,
        user_id=message.from_id,
        content=f"{liker.first_name} liked you message!",
        type="message_like",
        link_to=f"conversation/{liker.id}",
    )
