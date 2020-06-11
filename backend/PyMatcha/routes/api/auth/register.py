"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/gmorer
    <jlasne@student.42.fr> - <gmorer@student.42.fr>

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
import os

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request
from PyMatcha.models.user import User
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import ConflictError
from PyMatcha.utils.mail import send_mail_html
from PyMatcha.utils.success import SuccessOutputMessage


REQUIRED_KEYS_USER_CREATION = {"username": str, "email": str, "password": str, "first_name": str, "last_name": str}

auth_register_bp = Blueprint("auth_register", __name__)


@auth_register_bp.route("/auth/register", methods=["POST"])
@validate_params(REQUIRED_KEYS_USER_CREATION)
def api_create_user():
    current_app.logger.debug("/auth/register -> Call")
    data = request.get_json()
    data["email"] = data["email"].lower()
    try:
        current_app.logger.debug("Trying to register new user {}, {}".format(data["email"], data["username"]))
        new_user = User.register(
            email=data["email"],
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
    except ConflictError as e:
        current_app.logger.warning("Conflict error on user register: {}".format(e))
        raise e
    else:
        token = generate_confirmation_token(email=data["email"], token_type="confirm")
        link = os.getenv("APP_URL") + "/auth/confirm/" + token
        rendered_html = render_template("confirm_email.html", link=link)
        send_mail_html.delay(dest=data["email"], subject="Confirm your email on PyMatcha", html=rendered_html)
        return SuccessOutputMessage("email", new_user.email, "New user successfully created.")
