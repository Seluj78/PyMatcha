# coding=utf-8

"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/nbeny
    <jlasne@student.42.fr> - <nbeny@student.42.fr>

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

from flask import Flask

from PyMatcha.routes.views.home import home_bp

if os.environ.get("FLASK_ENV", None) == "dev":
    os.environ['FLASK_DEBUG'] = '1'
    os.environ['FLASK_SECRET_KEY'] = "ThisIsADevelopmentKey"

if "FLASK_DEBUG" not in os.environ:
    raise EnvironmentError("Debug bool is not set in the server's environment. Please fix and restart the server.")

if "FLASK_SECRET_KEY" not in os.environ:
    raise EnvironmentError("Secret key is not set in the server's environment. Please fix and restart the server.")

application = Flask(__name__)
application.debug = os.environ.get("FLASK_DEBUG", 1)
application.secret_key = os.environ.get("FLASK_SECRET_KEY", "ThisIsADevelopmentKey")

application.register_blueprint(home_bp)
