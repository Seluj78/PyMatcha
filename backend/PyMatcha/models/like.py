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

from PyMatcha.utils import create_likes_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Like(Model):
    table_name = "likes"

    id = Field(int, modifiable=False)
    liker_id = Field(int)
    liked_id = Field(int)
    dt_liked = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    is_superlike = Field(bool)

    @staticmethod
    def create(
        liker_id: int, liked_id: int, is_superlike: bool = False, dt_liked: Optional[datetime.datetime] = None
    ) -> Like:
        if not dt_liked:
            dt_liked = datetime.datetime.utcnow()
        new_like = Like(liker_id=liker_id, liked_id=liked_id, is_superlike=is_superlike, dt_liked=dt_liked)
        new_like.save()
        logging.debug("Creating new like")
        return new_like

    @classmethod
    def create_table(cls):
        create_likes_table(cls.db)
