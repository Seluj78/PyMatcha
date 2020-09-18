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
import os

import pymysql
from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from PyMatcha.utils.logging import setup_logging
from PyMatcha.utils.tables import create_tables
from pymysql.cursors import DictCursor
from redis import StrictRedis

PYMATCHA_ROOT = os.path.join(os.path.dirname(__file__), "../..")  # refers to application_top
dotenv_path = os.path.join(PYMATCHA_ROOT, ".env")
load_dotenv(dotenv_path)

REQUIRED_ENV_VARS = [
    "FLASK_DEBUG",
    "FLASK_SECRET_KEY",
    "FRONT_STATIC_FOLDER",
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "MAIL_PASSWORD",
    "APP_URL",
    "ENABLE_LOGGING",
    "DEBUG_AUTH_TOKEN",
]

for item in REQUIRED_ENV_VARS:
    if item not in os.environ:
        raise EnvironmentError(f"{item} is not set in the server's environment or .env file. It is required.")

if os.getenv("ENABLE_LOGGING") == "True":
    setup_logging()

application = Flask(__name__)

if os.getenv("FLASK_DEBUG", "false") == "true" or os.getenv("FLASK_DEBUG", "false") == "1":
    application.debug = True
else:
    application.debug = False

application.secret_key = os.getenv("FLASK_SECRET_KEY")
application.config.update(FLASK_SECRET_KEY=os.getenv("FLASK_SECRET_KEY"))
application.config["JWT_SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")

logging.debug("Configuring Celery Redis URLs")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
# Celery configuration
application.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
application.config["CELERY_RESULT_BACKEND"] = CELERY_RESULT_BACKEND

logging.debug("Initializing Celery")
# Initialize Celery
celery = Celery(application.name, broker=CELERY_BROKER_URL)
celery.conf.update(application.config)

logging.debug("Configuring JWT")

ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_TOKEN_EXPIRES
application.config["JWT_REFRESH_TOKEN_EXPIRES"] = REFRESH_TOKEN_EXPIRES
application.config["JWT_BLACKLIST_ENABLED"] = True
application.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

jwt = JWTManager(application)

logging.debug("Configuring JWT expired token handler callback")


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    logging.debug("Token {} expired".format(expired_token))
    resp = {
        "code": 401,
        "error": {
            "message": f"The {expired_token['type']} token has expired",
            "name": "Unauthorized Error",
            "solution": "Try again when you have renewed your token",
            "type": "UnauthorizedError",
        },
        "success": False,
    }
    return jsonify(resp), 401


logging.debug("Configuring CORS")
CORS(application, expose_headers="Authorization", supports_credentials=True)

if os.getenv("CI"):
    database_password = ""
else:
    database_password = os.getenv("DB_PASSWORD")

logging.debug("Setting database config from environment variables")
database_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": database_password,
    "db": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
}

logging.debug("Connecting to database")
db = pymysql.connect(**database_config)

logging.debug("Creating tables")
create_tables(db)

logging.debug("Configuring mail settings")
application.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="pymatcha@gmail.com",
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEBUG=False,
    MAIL_DEFAULT_SENDER="pymatcha@gmail.com",
)
logging.debug("Configuring mail")
mail = Mail(application)

redis = StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379), decode_responses=True, db=2
)

redis.flushdb()

from PyMatcha.models.user import get_user


logging.debug("Configuring JWT user callback loader")


from PyMatcha.utils.errors import NotFoundError


@jwt.user_loader_callback_loader
def jwt_user_callback(identity):
    try:
        u = get_user(identity["id"])
    except NotFoundError:
        # The user who the server issues the token for was deleted in the db.
        return None
    redis.set("online_user:" + str(identity["id"]), datetime.datetime.utcnow().timestamp())
    return u


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token["jti"]
    entry = redis.get("is_revoked_jti:" + jti)
    if entry is None:
        return True
    return entry == "true"


from PyMatcha.routes.api.user import user_bp
from PyMatcha.routes.api.auth.email import auth_email_bp
from PyMatcha.routes.api.auth.password import auth_password_bp
from PyMatcha.routes.api.auth.register import auth_register_bp
from PyMatcha.routes.api.auth.login import auth_login_bp
from PyMatcha.routes.api.profile.view import profile_view_bp
from PyMatcha.routes.api.profile.edit import profile_edit_bp
from PyMatcha.routes.api.profile.complete import profile_complete_bp
from PyMatcha.routes.api.profile.report import profile_report_bp
from PyMatcha.routes.api.like import like_bp
from PyMatcha.routes.api.match import match_bp
from PyMatcha.routes.api.messages import messages_bp
from PyMatcha.routes.api.recommendations import recommendations_bp

logging.debug("Registering Flask blueprints")
application.register_blueprint(user_bp)
application.register_blueprint(auth_email_bp)
application.register_blueprint(auth_password_bp)
application.register_blueprint(auth_register_bp)
application.register_blueprint(auth_login_bp)
application.register_blueprint(profile_view_bp)
application.register_blueprint(profile_edit_bp)
application.register_blueprint(profile_complete_bp)
application.register_blueprint(profile_report_bp)
application.register_blueprint(like_bp)
application.register_blueprint(match_bp)
application.register_blueprint(messages_bp)
application.register_blueprint(recommendations_bp)

if application.debug:
    logging.debug("Registering debug route")
    from PyMatcha.routes.api.debug import debug_bp

    application.register_blueprint(debug_bp)


@jwt.unauthorized_loader
def no_jwt_callback(error_message):
    return (
        jsonify(
            {
                "code": 401,
                "error": {
                    "message": error_message,
                    "name": "Unauthorized Error",
                    "solution": "Try again",
                    "type": "UnauthorizedError",
                },
                "success": False,
            }
        ),
        401,
    )


# import tasks here to be registered by celery

import PyMatcha.utils.tasks  # noqa
