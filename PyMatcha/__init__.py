# coding=utf-8

"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/ynacache
    <jlasne@student.42.fr> - <ynacache@student.42.fr>

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

from flask import Flask

from flask_admin import Admin

if os.environ.get("FLASK_ENV", None) == "dev":
    os.environ["FLASK_DEBUG"] = "1"
    os.environ["FLASK_SECRET_KEY"] = "ThisIsADevelopmentKey"

if "FLASK_DEBUG" not in os.environ:
    raise EnvironmentError("FLASK_DEBUT is not set in the server's environment. Please fix and restart the server.")

if "FLASK_SECRET_KEY" not in os.environ:
    raise EnvironmentError(
        "FLASK_SECRET_KEY is not set in the server's environment. Please fix and restart the server."
    )

if "DB_USER" not in os.environ:
    raise EnvironmentError("DB_USER is not set in the server's environment. Please fix and restart the server.")

if "DB_PASSWORD" not in os.environ:
    raise EnvironmentError("DB_PASSWORD is not set in the server's environment. Please fix and restart the server.")

application = Flask(__name__)
application.debug = os.environ.get("FLASK_DEBUG", 1)
application.secret_key = os.environ.get("FLASK_SECRET_KEY", "ThisIsADevelopmentKey")

app_db = peewee.MySQLDatabase(
    "PyMatcha",
    password=os.environ.get("DB_PASSWORD", None),
    user=os.environ.get("DB_USER", None),
    # TODO: Add DB host to env var
    host="pymatchadb.cvesmjtn6kz7.eu-west-3.rds.amazonaws.com",
    port=3306,
)

application.config["FLASK_ADMIN_SWATCH"] = "simplex"
admin = Admin(application, name="PyMatcha Admin", template_mode="bootstrap3")

from PyMatcha.models.user import User, UserAdmin

admin.add_view(UserAdmin(User))

from PyMatcha.routes.views.home import home_bp

application.register_blueprint(home_bp)

User.drop_table()
User.create_table()
