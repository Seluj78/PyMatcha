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

from PyMatcha import application
from PyMatcha.errors.template import generate_error_json


class UnauthorizedError(Exception):
    """
    This is the UnauthorizedError class for the Exception.
    """

    def __init__(self, msg: str, solution: str) -> None:
        self.name = "Unauthorized Error"
        self.msg = msg
        self.solution = solution
        self.status_code = 401

    pass


@application.errorhandler(UnauthorizedError)  # type: ignore
def generate_unauthorized(error: UnauthorizedError) -> dict:
    """
    This is the 401 response creator. It will create a 401 response with
    a custom message and the 401 code.

    :param error: The error body
    :return: Returns the response formatted
    """

    return generate_error_json(error, 401)
