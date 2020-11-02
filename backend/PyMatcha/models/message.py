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
from typing import Dict
from typing import Optional

from PyMatcha.utils import create_messages_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model
from timeago import format as timeago_format


class Message(Model):
    table_name = "messages"

    id = Field(int, modifiable=False)
    from_id = Field(int)
    to_id = Field(int)
    timestamp = Field(datetime, fmt="%Y-%m-%d %H:%M:%S")
    seen_timestamp = Field(datetime, fmt="%Y-%m-%d %H:%M:%S")
    content = Field(str)
    is_seen = Field(bool)
    is_liked = Field(bool)

    @staticmethod
    def create(
        from_id: int,
        to_id: int,
        content: str,
        timestamp: Optional[datetime] = None,
        seen_timestamp: Optional[datetime] = None,
        is_seen: bool = False,
        is_liked: bool = False,
    ) -> Message:
        if not timestamp:
            timestamp = datetime.utcnow()
        if not seen_timestamp:
            seen_timestamp = datetime.utcnow()
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

    def to_dict(self) -> Dict:
        returned_dict = super().to_dict()
        returned_dict["timestamp_ago"] = timeago_format(self.timestamp, datetime.utcnow())
        if self.seen_timestamp:
            returned_dict["seen_timestamp_ago"] = timeago_format(self.seen_timestamp, datetime.utcnow())
        else:
            returned_dict["seen_timestamp_ago"] = None

        return returned_dict

    @classmethod
    def create_table(cls):
        create_messages_table(cls.db)
