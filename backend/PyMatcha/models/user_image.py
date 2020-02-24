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

from typing import Dict

from datetime import datetime

from PyMatcha.utils.orm import Model, Field
from PyMatcha.utils import create_user_images_table

from PyMatcha.errors import NotFoundError


class UserImage(Model):
    table_name = "user_images"

    id = Field(int, modifiable=False)
    user_id = Field(int)
    description = Field(str)
    timestamp = Field(str)
    is_primary = Field(bool)

    def before_init(self, data):
        pass

    def delete(self):
        if self.id:
            with self.db.cursor() as c:
                c.execute(
                    """
                UPDATE {0} SET deleted = 1 
                WHERE id=CAST({1} AS INT)
                """.format(
                        self.table_name, self.id
                    )
                )
                self.db.commit()
        else:
            raise NotFoundError("Image not in database", "Try again")

    @staticmethod
    def create(
        user_id: int, description="", timestamp=datetime.timestamp(datetime.utcnow()), is_primary=False
    ) -> UserImage:
        new_image = UserImage(user_id=user_id, description=description, timestamp=str(timestamp), is_primary=is_primary)
        new_image.save()
        return new_image

    def get_all_info(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "timestamp": self.timestamp,
            "is_primary": self.is_primary,
        }

    @classmethod
    def create_table(cls):
        create_user_images_table(cls.db)
