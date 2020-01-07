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
from flask import Blueprint, send_from_directory

home_bp = Blueprint("home", __name__)


# Serve React App
@home_bp.route('/', defaults={'path': ''})
@home_bp.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(home_bp.static_folder + '/' + path):
        return send_from_directory(home_bp.static_folder, path)
    else:
        return send_from_directory(home_bp.static_folder, 'index.html')
