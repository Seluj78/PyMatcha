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
from datetime import datetime
from typing import Dict

import PyMatcha.models.user as user_module
from PyMatcha.utils import create_messages_table
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Message(Model):
    table_name = "messages"

    id = Field(int, modifiable=False)
    from_id = Field(int)
    to_id = Field(int)
    timestamp = Field(datetime)
    seen_timestamp = Field(datetime)
    content = Field(str)
    is_seen = Field(bool)
    is_liked = Field(bool)

    def before_init(self, data):
        pass

    @staticmethod
    def create(
        from_id: int,
        to_id: int,
        content: str,
        timestamp: datetime = datetime.utcnow(),
        seen_timestamp: datetime = None,
        is_seen: bool = False,
        is_liked: bool = False,
    ) -> Message:

        try:
            user_module.get_user(from_id)
        except NotFoundError:
            raise NotFoundError("User from_id {} not found".format(from_id), "Try again")

        try:
            user_module.get_user(to_id)
        except NotFoundError:
            raise NotFoundError("User to_id {} not found".format(to_id), "Try again")

        if not content:
            raise ValueError("content must not be empty")

        new_message = Message(
            from_id=from_id,
            to_id=to_id,
            content=content,
            timestamp=timestamp,
            seen_timestamp=seen_timestamp,
            is_seen=is_seen,
            is_liked=is_liked,
        )
        new_message.save()
        logging.debug("Created new message")
        return new_message

    def get_all_info(self) -> Dict:
        logging.debug("Returning all info on message {}".format(self.id))
        return {
            "id": self.id,
            "from_id": self.from_id,
            "to_id": self.to_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "seen_timestamp": self.seen_timestamp,
            "is_seen": self.is_seen,
            "is_liked": self.is_liked,
        }

    @classmethod
    def create_table(cls):
        create_messages_table(cls.db)
