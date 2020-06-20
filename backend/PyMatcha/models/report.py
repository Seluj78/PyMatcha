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

import datetime
import logging

from PyMatcha.utils import create_reports_table
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class Report(Model):
    table_name = "reports"

    id = Field(int, modifiable=False)
    reporter_id = Field(int)
    reported_id = Field(int)
    dt_reported = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    details = Field(str)
    reason = Field(str)
    status = Field(str)

    @staticmethod
    def create(
        reported_id: int,
        reporter_id: int,
        reason: str,
        details: str = None,
        dt_reported: datetime.datetime = datetime.datetime.utcnow(),
    ) -> Report:
        new_report = Report(
            reported_id=reported_id, reporter_id=reporter_id, reason=reason, details=details, dt_reported=dt_reported
        )
        new_report.save()
        logging.debug("Creating new report")
        return new_report

    @classmethod
    def create_table(cls):
        create_reports_table(cls.db)
