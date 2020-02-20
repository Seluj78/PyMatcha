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


class ConflictError(Exception):
    """
    This is the ConflictError class for the Exception.
    """

    def __init__(self, msg: str, solution: str) -> None:
        self.name = "Conflict Error"
        self.msg = msg
        self.solution = solution
        self.status_code = 409

    pass


@application.errorhandler(ConflictError)  # type: ignore
def generate_conflict(error: ConflictError) -> dict:
    """
    This is the 409 response creator. It will create a 409 response along with
    a custom message and the 409 code

    :param error: The error body
    :return: Returns the response formatted
    """

    return generate_error_json(error, 409)
