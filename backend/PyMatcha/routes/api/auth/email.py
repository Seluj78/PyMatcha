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
import datetime
import logging

from flask import Blueprint
from flask import render_template
from flask import request
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from PyMatcha.models.user import get_user
from PyMatcha.utils.confirm_token import confirm_token
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.mail import send_mail_html
from PyMatcha.utils.static import FRONTEND_EMAIL_CONFIRMATION_URL
from PyMatcha.utils.success import Success


REQUIRED_KEYS_NEW_EMAIL_CONF = {"email": str}

auth_email_bp = Blueprint("auth_email", __name__)


@auth_email_bp.route("/auth/confirm/<token>", methods=["POST"])
def confirm_email(token):
    try:
        email, token_type = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            logging.debug(f"Signature Expired for token {token}")
            raise BadRequestError("Signature Expired.", "Request another email confirmation and try again.")
        else:
            logging.debug(f"Bad Expired for token {token}")
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        if token_type != "confirm":
            logging.debug(f"Wrong token type for token {token}")
            raise BadRequestError("Wrong token type.")
        try:
            u = get_user(email)
        except NotFoundError:
            raise NotFoundError("User not found.")
        if u.is_confirmed:
            logging.debug("User already confirmed")
            raise BadRequestError("Email already confirmed.", "")
        else:
            u.is_confirmed = True
            u.confirmed_on = datetime.datetime.utcnow()
            u.save()
        logging.debug(f"User {u.id} confirmed.")
        return Success("Confirmation successful.")


@auth_email_bp.route("/auth/confirm/new", methods=["POST"])
@validate_params(REQUIRED_KEYS_NEW_EMAIL_CONF)
def request_new_email_conf():
    data = request.get_json()
    email = data["email"]
    try:
        u = get_user(email)
    except NotFoundError:
        pass
    else:
        if u.is_confirmed:
            logging.debug("Already confirmed.")
        else:
            logging.debug("/auth/confirm/new -> User found, sending new confirmation email")
            token = generate_confirmation_token(email=email, token_type="confirm")
            link = FRONTEND_EMAIL_CONFIRMATION_URL + token
            rendered_html = render_template("confirm_email.html", link=link)
            send_mail_html.delay(dest=data["email"], subject="Confirm your email on Matcha", html=rendered_html)
    logging.debug("/auth/confirm/new -> New confirmation email sent if user exists in database")
    return Success("New confirmation email sent if user exists in database and isn't already confirmed.")
