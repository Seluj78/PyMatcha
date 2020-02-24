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

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from PyMatcha import application


def generate_confirmation_token(email, token_type):
    if token_type not in ["confirm", "reset"]:
        raise ValueError("Reset token type must be confirm or reset")
    serializer = URLSafeTimedSerializer(application.config["FLASK_SECRET_KEY"])
    return serializer.dumps(email + ":{}".format(token_type), salt=application.config["FLASK_SECRET_KEY"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(application.config["FLASK_SECRET_KEY"])
    try:
        ret = serializer.loads(token, salt=application.config["FLASK_SECRET_KEY"], max_age=expiration)
        email = ret.split(":")[0]
        token_type = ret.split(":")[1]
    except (SignatureExpired, BadSignature) as e:
        raise e
    return email, token_type
