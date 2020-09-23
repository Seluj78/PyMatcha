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
import logging

DISABLE_SQL_NOTES = """SET sql_notes = 0;"""
ENABLE_SQL_NOTES = """SET sql_notes = 1;"""


def _create_user_table(db):
    with db.cursor() as c:
        logging.info("Creating table users.")
        c.execute(DISABLE_SQL_NOTES)
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
        bio                  LONGTEXT DEFAULT NULL,
        gender               ENUM('male', 'female', 'other'),
        orientation          ENUM('heterosexual', 'homosexual', 'bisexual', 'other'),
        birthdate            DATE DEFAULT NULL,
        geohash              VARCHAR(256) DEFAULT NULL,
        heat_score           INT DEFAULT NULL,
        date_joined          DATETIME DEFAULT NOW(),
        date_lastseen        DATETIME DEFAULT NOW(),
        previous_reset_token VARCHAR(256),
        is_online            BOOLEAN DEFAULT (FALSE),
        is_profile_completed BOOLEAN DEFAULT (FALSE),
        is_confirmed         BOOLEAN DEFAULT (FALSE),
        confirmed_on         DATETIME DEFAULT NULL
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_tags_table(db):
    with db.cursor() as c:
        logging.info("Creating table tags.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS tags
        (
        id            INT auto_increment PRIMARY KEY,
        user_id       INT NOT NULL,
        name          VARCHAR(256)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_views_table(db):
    with db.cursor() as c:
        logging.info("Creating table views.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS views
        (
        id            INT auto_increment PRIMARY KEY,
        profile_id    INT NOT NULL,
        viewer_id     INT NOT NULL,
        dt_seen       DATETIME DEFAULT NOW()
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_reports_table(db):
    with db.cursor() as c:
        logging.info("Creating table reports.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS reports
        (
        id            INT auto_increment PRIMARY KEY,
        reported_id   INT NOT NULL,
        reporter_id   INT NOT NULL,
        dt_reported   DATETIME DEFAULT NOW(),
        details       VARCHAR(256),
        reason        ENUM('harassment', 'bot', 'spam', 'inappropriate content'),
        status        ENUM('processing request', 'insufficient evidence', 'convicted and banned')
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_likes_table(db):
    with db.cursor() as c:
        logging.info("Creating table likes.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS likes
        (
        id            INT auto_increment PRIMARY KEY,
        liked_id      INT NOT NULL,
        liker_id      INT NOT NULL,
        dt_liked      DATETIME DEFAULT NOW(),
        is_superlike  BOOLEAN DEFAULT FALSE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_matches_table(db):
    with db.cursor() as c:
        logging.info("Creating table matches.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS matches
        (
        id            INT auto_increment PRIMARY KEY,
        user_1        INT NOT NULL,
        user_2        INT NOT NULL,
        dt_matched    DATETIME DEFAULT NOW()
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_messages_table(db):
    with db.cursor() as c:
        logging.info("Creating table messages.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS messages
        (
        id             INT auto_increment PRIMARY KEY,
        from_id        INT NOT NULL,
        to_id          INT NOT NULL,
        timestamp      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        seen_timestamp TIMESTAMP,
        content        LONGTEXT NOT NULL,
        is_liked       BOOLEAN DEFAULT FALSE,
        is_seen        BOOLEAN DEFAULT FALSE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def _create_images_table(db):
    with db.cursor() as c:
        logging.info("Creating table images.")
        c.execute(DISABLE_SQL_NOTES)
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS images
        (
        id             INT auto_increment PRIMARY KEY,
        user_id        INT NOT NULL,
        timestamp      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        link           VARCHAR(256) NOT NULL,
        is_primary       BOOLEAN DEFAULT FALSE
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
        """
        )
        c.execute(ENABLE_SQL_NOTES)
        c.close()


def create_tables(db):
    _create_user_table(db)
    _create_tags_table(db)
    _create_views_table(db)
    _create_reports_table(db)
    _create_likes_table(db)
    _create_matches_table(db)
    _create_messages_table(db)
    _create_images_table(db)
