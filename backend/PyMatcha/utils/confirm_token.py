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

from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from itsdangerous import URLSafeTimedSerializer
from PyMatcha import application

ACCEPTED_TOKEN_TYPES = ["confirm", "reset"]


def generate_confirmation_token(email, token_type):
    logging.debug("Generating confirmation token for email {}".format(email))
    if token_type not in ACCEPTED_TOKEN_TYPES:
        logging.error("token_type must be of {} and is {}".format(ACCEPTED_TOKEN_TYPES, token_type))
        raise ValueError("Reset token type must be confirm or reset.")
    serializer = URLSafeTimedSerializer(application.config["FLASK_SECRET_KEY"])
    token = serializer.dumps(email + ":{}".format(token_type), salt=application.config["FLASK_SECRET_KEY"])
    logging.debug("Generated token {} for email {}".format(token, email))
    return token


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(application.config["FLASK_SECRET_KEY"])
    try:
        logging.debug("Trying to confirm token {}")
        ret = serializer.loads(token, salt=application.config["FLASK_SECRET_KEY"], max_age=expiration)
        email = ret.split(":")[0]
        token_type = ret.split(":")[1]
    except (SignatureExpired, BadSignature) as e:
        raise e
    logging.debug("Confirmed token {} for email {} of type {}".format(token, email, token_type))
    return email, token_type
