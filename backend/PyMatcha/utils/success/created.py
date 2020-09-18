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
from flask import jsonify


def SuccessCreated(message: str) -> dict:
    """
    Will generate a SuccessCreated message with the appropriate return code and jsonify it.

    :param message: The message to include

    :return: Returns a json response
    """

    status_code = 201
    success = True
    json = {"success": success, "message": message, "code": status_code}
    resp = jsonify(json)
    resp.status_code = status_code

    return resp
