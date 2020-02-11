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

import peewee

from flask import Flask, send_from_directory

from flask_admin import Admin

from flask_cors import CORS

from dotenv import load_dotenv


PYMATCHA_ROOT = os.path.join(os.path.dirname(__file__), '../..')   # refers to application_top
dotenv_path = os.path.join(PYMATCHA_ROOT, '.env')
load_dotenv(dotenv_path)


REQUIRED_ENV_VARS = [
    "FLASK_DEBUG",
    "FLASK_SECRET_KEY",
    "FRONT_STATIC_FOLDER",
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
]

for item in REQUIRED_ENV_VARS:
    if item not in os.environ:
        raise EnvironmentError(f"{item} is not set in the server's environment or .env file. It is required")

# TODO: Set static folder to env var or conf
application = Flask(__name__, static_folder=os.getenv("FRONT_STATIC_FOLDER"))
application.debug = os.getenv("FLASK_DEBUG")
application.secret_key = os.getenv("FLASK_SECRET_KEY")

app_db = peewee.MySQLDatabase(
    "PyMatcha",
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    password=os.getenv("DB_PASSWORD"),
    user=os.getenv("DB_USER")
)

application.config["FLASK_ADMIN_SWATCH"] = "simplex"
admin = Admin(application, name="PyMatcha Admin", template_mode="bootstrap3")

CORS(application)

from PyMatcha.models.user import User, UserAdmin

admin.add_view(UserAdmin(User))

from PyMatcha.routes.api.ping_pong import ping_pong_bp

application.register_blueprint(ping_pong_bp)

if bool(int(os.environ.get("CI", 0))):
    User.drop_table()
    User.create_table()


# Serve React App
@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(application.static_folder + '/' + path):
        return send_from_directory(application.static_folder, path)
    else:
        return send_from_directory(application.static_folder, 'index.html')
