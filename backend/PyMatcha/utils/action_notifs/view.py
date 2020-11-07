import logging

from PyMatcha.models.notification import Notification
from PyMatcha.models.user import User
from PyMatcha.models.view import View


def do_view(viewer_user: User, viewed_user_id: int):
    logging.debug(f"{viewer_user.id} viewed {viewed_user_id}")
    View.create(profile_id=viewed_user_id, viewer_id=viewer_user.id)
    Notification.create(
        trigger_id=viewer_user.id,
        user_id=viewed_user_id,
        content=f"{viewer_user.first_name} just viewed your profile! Go check their profile out!",
        type="view",
        link_to=f"users/{viewer_user.id}",
    )
