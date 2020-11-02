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
from PyMatcha.utils.errors.badrequest import BadRequestError
from PyMatcha.utils.errors.conflict import ConflictError
from PyMatcha.utils.errors.forbidden import ForbiddenError
from PyMatcha.utils.errors.notfound import NotFoundError
from PyMatcha.utils.errors.unauthorized import UnauthorizedError

__all__ = ["BadRequestError", "ConflictError", "ForbiddenError", "NotFoundError", "UnauthorizedError"]
