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
from __future__ import annotations

import datetime
import logging
from typing import Optional

from PyMatcha.utils import create_matches_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Match(Model):
    table_name = "matches"

    id = Field(int, modifiable=False)
    user_1 = Field(int)
    user_2 = Field(int)
    dt_matched = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create(user_1: int, user_2: int, dt_matched: Optional[datetime.datetime] = None) -> Match:
        if not dt_matched:
            dt_matched = datetime.datetime.utcnow()
        new_match = Match(user_1=user_1, user_2=user_2, dt_matched=dt_matched)
        new_match.save()
        logging.debug("Creating new match")
        return new_match

    @classmethod
    def create_table(cls):
        create_matches_table(cls.db)
