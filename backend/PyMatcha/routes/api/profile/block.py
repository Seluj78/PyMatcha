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
from PyMatcha.models.block import Block
from PyMatcha.models.user import get_user
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success

profile_block_bp = Blueprint("profile_block", __name__)


@profile_block_bp.route("/profile/block/<uid>", methods=["POST"])
@jwt_required
def block_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    if current_user.id == u.id:
        current_app.logger.info(f"User {current_user.id} tried to block itself")
        raise BadRequestError("Cannot block yourself.")
    if not Block.get_multi(blocker_id=current_user.id, blocked_id=u.id):
        Block.create(blocker_id=current_user.id, blocked_id=u.id)
        current_app.logger.info(f"Block successfull from {current_user.id} to {u.id}")
        return Success(f"Successfully blocked {u.id}.")
    else:
        current_app.logger.info(f"{current_user.id} already blocked {u.id}")
        raise BadRequestError("You already blocked this user.")


@profile_block_bp.route("/profile/unblock/<uid>", methods=["POST"])
@jwt_required
def unblock_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found.")
    block = Block.get_multi(blocker_id=current_user.id, blocked_id=u.id)
    if not block:
        current_app.logger.info(f"{current_user.id} tried to unblock {u.id} but never blocked it first")
        raise BadRequestError("You didn't block this user.")
    else:
        block.delete()
        current_app.logger.info(f"Unblock successfull from {current_user.id} to {u.id}")
        return Success("Unblock successful.")
