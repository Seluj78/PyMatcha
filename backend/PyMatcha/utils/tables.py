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


def _create_user_table(db):
    with db.cursor() as c:
        print("Creating table users.")
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS users 
        (
        id            INT auto_increment PRIMARY KEY,
        first_name    VARCHAR(256) NOT NULL,
        last_name     VARCHAR(256),
        email         VARCHAR(256) NOT NULL UNIQUE,
        username      VARCHAR(256) NOT NULL UNIQUE,
        password      LONGTEXT NOT NULL,
        bio           LONGTEXT,
        gender        ENUM('male', 'female', 'other'),
        orientation   ENUM('heterosexual', 'homosexual', 'bisexual'),
        birthdate     DATE,
        geohash       VARCHAR(256),
        tags          LONGTEXT,
        heat_score    INT DEFAULT (0),
        online        BOOLEAN DEFAULT (FALSE),
        date_joined   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_lastseen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deleted       BOOLEAN DEFAULT (FALSE)
        )
        """
        )


def create_tables(db):
    _create_user_table(db)
