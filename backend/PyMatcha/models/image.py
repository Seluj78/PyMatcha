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

import logging
from datetime import datetime
from typing import Optional

from PyMatcha.utils import create_images_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Image(Model):
    table_name = "images"

    id = Field(int, modifiable=False)
    user_id = Field(int)
    link = Field(str)
    dt_added = Field(datetime, fmt="%Y-%m-%d %H:%M:%S")
    is_primary = Field(bool)

    @staticmethod
    def create(user_id: int, link: str, is_primary: bool = False, dt_added: Optional[datetime] = None) -> Image:
        if not dt_added:
            dt_added = datetime.utcnow()
        new_image = Image(user_id=user_id, link=link, is_primary=is_primary, dt_added=dt_added)
        new_image.save()
        logging.debug("Creating new image")
        return new_image

    @classmethod
    def create_table(cls):
        create_images_table(cls.db)
