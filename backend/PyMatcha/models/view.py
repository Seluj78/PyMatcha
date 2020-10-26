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

from PyMatcha.utils import create_views_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class View(Model):
    table_name = "views"

    id = Field(int, modifiable=False)
    profile_id = Field(int)
    viewer_id = Field(int)
    dt_seen = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def create(profile_id: int, viewer_id: int, dt_seen: datetime.datetime = datetime.datetime.utcnow()) -> View:
        new_view = View(profile_id=profile_id, viewer_id=viewer_id, dt_seen=dt_seen)
        new_view.save()
        logging.debug("Creating new view")
        return new_view

    @classmethod
    def create_table(cls):
        create_views_table(cls.db)
