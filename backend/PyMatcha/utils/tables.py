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

import logging


def _create_user_table(db):
    with db.cursor() as c:
        logging.info("Creating table users.")
        c.execute("""SET sql_notes = 0;""")
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS users 
        (
        id                   INT auto_increment PRIMARY KEY,
        first_name           VARCHAR(256) NOT NULL,
        last_name            VARCHAR(256),
        email                VARCHAR(256) NOT NULL UNIQUE,
        username             VARCHAR(256) NOT NULL UNIQUE,
        password             LONGTEXT NOT NULL,
        bio                  LONGTEXT,
        gender               ENUM('male', 'female', 'other'),
        orientation          ENUM('heterosexual', 'homosexual', 'bisexual'),
        birthdate            DATE,
        geohash              VARCHAR(256),
        tags                 LONGTEXT,
        heat_score           INT DEFAULT (0),
        date_joined          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_lastseen        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        previous_reset_token VARCHAR(256),
        is_online            BOOLEAN DEFAULT (FALSE),
        is_profile_completed BOOLEAN DEFAULT (FALSE),
        is_confirmed         BOOLEAN DEFAULT (FALSE),
        confirmed_on         TIMESTAMP DEFAULT NULL
        );
        """
        )
        c.execute("""SET sql_notes = 1;""")


def _create_user_images_table(db):
    with db.cursor() as c:
        logging.info("Creating table user_images.")
        c.execute("""SET sql_notes = 0;""")
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS user_images
        (
        id            INT auto_increment PRIMARY KEY,
        user_id       INT NOT NULL,
        description   LONGTEXT,
        timestamp     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_primary    BOOLEAN NOT NULL
        )
        """
        )
        c.execute("""SET sql_notes = 1;""")


def create_tables(db):
    _create_user_table(db)
    _create_user_images_table(db)
