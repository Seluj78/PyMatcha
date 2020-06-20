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
import datetime
import os

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from PyMatcha.models.user import get_user
from PyMatcha.utils.confirm_token import confirm_token
from PyMatcha.utils.confirm_token import generate_confirmation_token
from PyMatcha.utils.decorators import validate_params
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.mail import send_mail_html
from PyMatcha.utils.success import Success


REQUIRED_KEYS_NEW_EMAIL_CONF = {"email": str}

auth_email_bp = Blueprint("auth_email", __name__)


@auth_email_bp.route("/auth/confirm/<token>", methods=["GET"])
def confirm_email(token):
    current_app.logger.debug("/auth/confirm/{} -> Call".format(token))
    try:
        email, token_type = confirm_token(token, expiration=7200)
    except (SignatureExpired, BadSignature) as e:
        if e == SignatureExpired:
            current_app.logger.debug("/auth/confirm -> Signature Expired")
            return redirect("/?type=confirm&success=false&message=Signature expired")
        else:
            current_app.logger.debug("/auth/confirm -> Bad Expired")
            return redirect("/?type=confirm&success=false&message=Bad Signature")
    else:
        if token_type != "confirm":
            current_app.logger.debug("/auth/confirm -> Wrong token type")
            return redirect("/?type=confirm&success=false&message=Wrong token type")
        try:
            u = get_user(email)
        except NotFoundError:
            current_app.logger.debug("/auth/confirm -> User not found")
            return redirect("/?type=confirm&success=false&message=User not found")
        if u.is_confirmed:
            current_app.logger.debug("/auth/confirm -> User already confirmed")
            return redirect("/?type=confirm&success=false&message=User already confirmed")
        else:
            u.is_confirmed = True
            u.confirmed_on = datetime.datetime.utcnow()
            u.save()
        current_app.logger.debug("/auth/confirm -> User {} confirmed.".format(u.id))
        return redirect("/?type=confirm&success=true&message=User confirmed")


@auth_email_bp.route("/auth/confirm/new", methods=["POST"])
@validate_params(REQUIRED_KEYS_NEW_EMAIL_CONF)
def request_new_email_conf():
    current_app.logger.debug("/auth/confirm/new -> Call")
    data = request.get_json()
    email = data["email"]
    try:
        u = get_user(email)
    except NotFoundError:
        current_app.logger.debug("/auth/confirm/new -> User not found")
        pass
    else:
        if u.is_confirmed:
            current_app.logger.debug("/auth/confirm/new -> User found, Already confirmed.")
            return Success("User already confirmed")
        else:
            current_app.logger.debug("/auth/confirm/new -> User found, sending new confirmation email")
            token = generate_confirmation_token(email=email, token_type="confirm")
            link = os.getenv("APP_URL") + "/auth/confirm/" + token
            rendered_html = render_template("confirm_email.html", link=link)
            send_mail_html.delay(dest=data["email"], subject="Confirm your email on PyMatcha", html=rendered_html)
    current_app.logger.debug("/auth/confirm/new -> New confirmation email sent if user exists in database")
    return Success("New confirmation email sent if user exists in database")
