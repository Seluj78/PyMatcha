import logging

from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.notification import Notification
from PyMatcha.models.user import User


def do_like(liker_user: User, liked_user_id: int):
    logging.debug(f"{liker_user.id} liked {liked_user_id}")
    Like.create(liker_id=liker_user.id, liked_id=liked_user_id, is_superlike=False)
    Notification.create(
        trigger_id=liker_user.id,
        user_id=liked_user_id,
        content=f"{liker_user.first_name} liked you! Go check them out!",
        type="like",
        link_to=f"users/{liker_user.id}",
    )


def do_superlike(liker_user: User, liked_user_id: int):
    logging.debug(f"{liker_user.id} superliked {liked_user_id}")
    Like.create(liker_id=liker_user.id, liked_id=liked_user_id, is_superlike=True)
    Notification.create(
        trigger_id=liker_user.id,
        user_id=liked_user_id,
        content=f"{liker_user.first_name} superliked you 😏! Go check them out!",
        type="superlike",
        link_to=f"users/{liker_user.id}",
    )


def do_match(liker_user: User, liked_user: User):
    logging.debug(f"{liker_user.id} and {liked_user.id} matched.")
    Match.create(user_1=liker_user.id, user_2=liked_user.id)
    Notification.create(
        trigger_id=liker_user.id,
        user_id=liked_user.id,
        content=f"You and {liker_user.first_name} matched!",
        type="match",
        link_to=f"conversation/{liker_user.id}",
    )
    Notification.create(
        trigger_id=liked_user.id,
        user_id=liker_user.id,
        content=f"You and {liked_user.username} matched!",
        type="match",
        link_to=f"conversation/{liked_user.id}",
    )


def do_unlike(unliker: User, unliked_id: int):
    logging.debug(f"{unliker.id} unliked {unliked_id}")
    Like.get_multi(liked_id=unliked_id, liker_id=unliker.id).delete()
    m1 = Match.get_multi(user_1=unliked_id, user_2=unliker.id)
    m2 = Match.get_multi(user_1=unliker.id, user_2=unliked_id)

    if m1:
        m1.delete()
    elif m2:
        m2.delete()
    if m1 or m2:
        logging.debug(f"{unliker.id} and {unliked_id} unmatched.")

    Notification.create(
        trigger_id=unliker.id,
        user_id=unliked_id,
        content=f"{unliker.first_name} unliked you.",
        type="unlike",
        link_to=None,
    )
