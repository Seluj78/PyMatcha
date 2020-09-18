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
import os

from flask import Blueprint
from flask import current_app
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
from PyMatcha.utils.success import Success


REQUIRED_KEYS_PASSWORD_FORGOT = {"email": str}
REQUIRED_KEYS_PASSWORD_RESET = {"token": str, "password": str}

auth_password_bp = Blueprint("auth_password", __name__)

# TODO: Test to reset password in postman


@auth_password_bp.route("/auth/password/forgot", methods=["POST"])
@validate_params(REQUIRED_KEYS_PASSWORD_FORGOT)
def forgot_password():
    current_app.logger.debug("/auth/password/forgot -> Call")
    data = request.get_json()
    try:
        get_user(data["email"])
    except NotFoundError:
        current_app.logger.debug("/auth/password/forgot -> User {} not found, no email sent".format(data["email"]))
        pass
    else:
        token = generate_confirmation_token(email=data["email"], token_type="reset")
        # link = os.getenv("APP_URL") + "/auth/password/forgot/" + token
        link = f"{os.getenv('FRONT_URL')}/accounts/password/reset?token={token}"
        rendered_html = render_template("password_reset.html", link=link)
        current_app.logger.debug("/auth/password/forgot -> Sending worker request to send email")
        send_mail_html.delay(dest=data["email"], subject="Reset your password on PyMatcha", html=rendered_html)
    current_app.logger.debug(
        "/auth/password/forgot -> Password reset mail sent successfully for user {}".format(data["email"])
    )
    return Success("Password reset mail sent successfully if user exists in DB")


@auth_password_bp.route("/auth/password/reset", methods=["POST"])
@validate_params(REQUIRED_KEYS_PASSWORD_RESET)
def reset_password():
    current_app.logger.debug("/auth/password/reset -> Call")
    data = request.get_json()
    try:
        email, token_type = confirm_token(data["token"], expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            current_app.logger.debug("/auth/password/reset -> Signature Expired")
            raise BadRequestError("Signature Expired.", "Request another password reset and try again.")
        else:
            current_app.logger.debug("/auth/password/reset -> Bad Signature")
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        if token_type != "reset":
            current_app.logger.debug("/auth/password/reset -> Wrong token type")
            raise BadRequestError("Wrong token type.")
        try:
            u = get_user(email)
        except NotFoundError:
            current_app.logger.debug("/auth/password/reset -> User not found")
            raise NotFoundError("User not found.")
        if u.previous_reset_token == data["token"]:
            current_app.logger.debug("/auth/password/reset -> Token already used")
            raise BadRequestError("Token already used", "Please request a new one.")
        u.password = hash_password(data["password"])
        u.previous_reset_token = data["token"]
        u.save()
        current_app.logger.debug("/auth/password/reset -> Password reset successfully")
        return Success("Password reset successful.")


@auth_password_bp.route("/auth/password/check_token", methods=["POST"])
@validate_params({"token": str})
def check_token_validity():
    data = request.get_json()
    try:
        confirm_token(data["token"], expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            current_app.logger.debug("/auth/password/reset -> Signature Expired")
            raise BadRequestError("Signature Expired.", "Request another password reset and try again.")
        else:
            current_app.logger.debug("/auth/password/reset -> Bad Signature")
            raise BadRequestError("Bad Signature.", "Request another password reset and try again.")
    else:
        return Success("Reset token is correct")
