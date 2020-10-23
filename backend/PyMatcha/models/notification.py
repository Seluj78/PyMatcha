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

from PyMatcha.utils import create_notifications_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Notification(Model):
    table_name = "notifications"

    id = Field(int, modifiable=False)
    dt_received = Field(datetime, fmt="%Y-%m-%d %H:%M:%S")
    content = Field(str)
    type = Field(str)
    is_seen = Field(bool)
    link_to = Field(str)

    @staticmethod
    def create(
        content: str, type: str, link_to: str, is_seen: bool = False, dt_received: datetime = datetime.utcnow()
    ) -> Notification:
        new_notif = Notification(content=content, type=type, link_to=link_to, is_seen=is_seen, dt_received=dt_received)
        new_notif.save()
        logging.debug("Creating new notification")
        return new_notif

    @classmethod
    def create_table(cls):
        create_notifications_table(cls.db)
