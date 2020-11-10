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
import logging

from flask import Blueprint
from flask import render_template
from flask import request
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from PyMatcha.models.user import get_user
from PyMatcha.utils import hash_password
from PyMatcha.utils.confirm_token import confirm_token
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.mail import send_mail_html
from PyMatcha.utils.static import FRONTEND_PASSWORD_RESET_URL
from PyMatcha.utils.success import Success

REQUIRED_KEYS_PASSWORD_FORGOT = {"email": str}
REQUIRED_KEYS_PASSWORD_RESET = {"token": str, "password": str}

auth_password_bp = Blueprint("auth_password", __name__)


@auth_password_bp.route("/auth/password/forgot", methods=["POST"])
@validate_params(REQUIRED_KEYS_PASSWORD_FORGOT)
def forgot_password():
    data = request.get_json()
    try:
        get_user(data["email"])
    except NotFoundError:
        logging.debug("User not found, no email sent")
        pass
    else:
        token = generate_confirmation_token(email=data["email"], token_type="reset")
        link = FRONTEND_PASSWORD_RESET_URL + token
        rendered_html = render_template("password_reset.html", link=link)
        logging.debug("Sending worker request to send email")
        send_mail_html.delay(dest=data["email"], subject="Reset your password on PyMatcha", html=rendered_html)
    logging.debug("Password reset mail sent successfully for user.")
    return Success("Password reset mail sent successfully if user exists in DB.")


@auth_password_bp.route("/auth/password/reset", methods=["POST"])
@validate_params(REQUIRED_KEYS_PASSWORD_RESET)
def reset_password():
    data = request.get_json()
    token = data["token"]
    try:
        email, token_type = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            logging.debug(f"Signature Expired for {token}")
            raise BadRequestError("Signature Expired.", "Request another password reset and try again.")
        else:
            logging.debug(f"Bad Signature for {token}")
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        if token_type != "reset":
            logging.debug(f"Wrong token type for {token}")
            raise BadRequestError("Wrong token type.")
        try:
            u = get_user(email)
        except NotFoundError:
            raise NotFoundError("User not found.")
        if u.previous_reset_token == token:
            logging.debug("Token already used")
            raise BadRequestError("Token already used", "Please request a new one.")
        u.password = hash_password(data["password"])
        u.previous_reset_token = token
        u.save()
        logging.debug("Password reset successfully")
        return Success("Password reset successful.")


@auth_password_bp.route("/auth/password/check_token", methods=["POST"])
@validate_params({"token": str})
def check_token_validity():
    data = request.get_json()
    token = data["token"]
    try:
        email, token_type = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            logging.debug(f"Signature Expired for {token}")
            raise BadRequestError("Signature Expired.", "Request another password reset and try again.")
        else:
            logging.debug(f"Bad Signature for {token}")
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        try:
            u = get_user(email)
        except NotFoundError:
            raise NotFoundError("User not found.")
        if u.previous_reset_token == token:
            logging.debug("Token already used")
            raise BadRequestError("Token already used", "Please request a new one.")
        return Success("Reset token is correct.")
