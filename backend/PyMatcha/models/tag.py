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
from __future__ import annotations

import logging

from PyMatcha.utils import create_tags_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Tag(Model):
    table_name = "tags"

    id = Field(int, modifiable=False)
    user_id = Field(int)
    name = Field(str)

    def before_init(self, data):
        pass

    @staticmethod
    def create(user_id: int, name="") -> Tag:
        new_tag = Tag(user_id=user_id, name=name)
        new_tag.save()
        logging.debug("Creating new tag")
        return new_tag

    @classmethod
    def create_table(cls):
        create_tags_table(cls.db)
