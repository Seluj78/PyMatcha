"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/gmorer
    <jlasne@student.42.fr> - <lauris.skraucis@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from flask import Blueprint
from flask import current_app
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.utils.success import SuccessOutput


history_bp = Blueprint("history", __name__)


@history_bp.route("/history/viewed")
@jwt_required
def history_viewed_people():
    viewed = [view.to_dict() for view in current_user.get_view_history()]
    current_app.logger.info(f"Returning viewed profiles for user {current_user.id}")
    return SuccessOutput("viewed", viewed)


@history_bp.route("/history/viewed/me", methods=["GET"])
@jwt_required
def history_viewed_me():
    viewed_people = [view.to_dict() for view in current_user.get_views()]
    current_app.logger.info(f"Returning profiles who viewed user {current_user.id}")
    return SuccessOutput("viewed_me", viewed_people)


@history_bp.route("/history/liked", methods=["GET"])
@jwt_required
def history_liked_people():
    liked = [like.to_dict() for like in current_user.get_likes_sent()]
    current_app.logger.info(f"Returning liked profiles for user {current_user.id}")
    return SuccessOutput("liked", liked)


@history_bp.route("/history/liked/me", methods=["GET"])
@jwt_required
def history_liked_me():
    liked_people = [like.to_dict() for like in current_user.get_likes_received()]
    current_app.logger.info(f"Returning profiles who liked user {current_user.id}")
    return SuccessOutput("liked_me", liked_people)


@history_bp.route("/history/blocked", methods=["GET"])
@jwt_required
def history_blocked():
    blocked_people = [block.to_dict() for block in current_user.get_blocks()]
    current_app.logger.info(f"Returning blocked profiles for user {current_user.id}")
    return SuccessOutput("blocked", blocked_people)
