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
import hashlib
import logging
from typing import Any
from typing import Dict
from typing import Optional

import Geohash
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.report import Report
from PyMatcha.models.tag import Tag
from PyMatcha.models.view import View
from PyMatcha.utils import create_user_table
from PyMatcha.utils import hash_password
from PyMatcha.utils.errors import ConflictError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.orm import Field
from PyMatcha.utils.orm import Model


class User(Model):
    table_name = "users"

    id = Field(int, modifiable=False)
    first_name = Field(str)
    last_name = Field(str)
    email = Field(str)
    username = Field(str)
    password = Field(str, hidden=True)
    bio = Field(str)
    gender = Field(str)
    orientation = Field(str)
    birthdate = Field(datetime.date)
    geohash = Field(str)
    heat_score = Field(int)
    is_online = Field(bool)
    date_joined = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    date_lastseen = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    is_profile_completed = Field(bool)
    is_confirmed = Field(bool)
    confirmed_on = Field(datetime.datetime, fmt="%Y-%m-%d %H:%M:%S")
    previous_reset_token = Field(str)

    def check_password(self, password: str) -> bool:
        logging.debug("Checking password again {} hashed password".format(self.id))
        _hash, salt = self.password.split(":")
        return _hash == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    @staticmethod
    def create(
        first_name: str,
        last_name: str,
        email: str,
        username: str,
        password: str,
        bio: str,
        gender: str,
        orientation: str,
        birthdate: datetime.date,
        geohash: str,
        heat_score: int = 0,
        is_online: bool = False,
        date_joined: datetime.datetime = datetime.datetime.utcnow(),
        date_lastseen: datetime.datetime = datetime.datetime.utcnow(),
        is_profile_completed: bool = False,
        is_confirmed: bool = False,
        confirmed_on: datetime.datetime = None,
    ) -> User:
        # Check email availability
        try:
            User.get(email=email)
        except ValueError:
            pass
        else:
            logging.error("Email {} taken".format(email))
            raise ConflictError("Email {} taken".format(email), "Use another email")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            logging.error("Username {} taken".format(username))
            raise ConflictError("Username {} taken".format(username), "Try another username")

        # Check correct gender
        if gender not in ["male", "female", "other"]:
            logging.error("Gender must be male, female or other, not {}".format(gender))
            raise ConflictError("Gender must be male, female or other, not {}".format(gender), "Try again")

        # Check correct orientation
        if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
            logging.error(
                "Sexual Orientation must be heterosexual, homosexual, bisexual or other, not {}".format(orientation)
            )
            raise ConflictError(
                "Sexual Orientation must be heterosexual, homosexual, bisexual or other, not {}".format(orientation),
                "Try again",
            )

        # Check correct geohash
        try:
            Geohash.decode(geohash)
        except ValueError as e:
            logging.error("Geohash error: {}".format(e))
            raise e

        # Encrypt password
        password = hash_password(password)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email.lower(),
            username=username,
            password=password,
            bio=bio,
            gender=gender,
            orientation=orientation,
            birthdate=birthdate,
            geohash=geohash,
            heat_score=heat_score,
            is_online=is_online,
            date_joined=date_joined,
            date_lastseen=date_lastseen,
            is_profile_completed=is_profile_completed,
            is_confirmed=is_confirmed,
            confirmed_on=confirmed_on,
            previous_reset_token=None,
        )
        new_user.save()
        logging.debug("New user {} created".format(new_user.email))
        return new_user

    @staticmethod
    def register(email: str, username: str, password: str, first_name: str, last_name: str) -> User:
        # Check email availability
        try:
            User.get(email=email)
        except ValueError:
            pass
        else:
            logging.debug("Email {} taken".format(email))
            raise ConflictError("Email {} taken".format(email), "Use another email")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            logging.error("Username {} taken".format(username))
            raise ConflictError("Username {} taken".format(username), "Try another username")

        # Encrypt password
        password = hash_password(password)

        new_user = User(
            email=email.lower(),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio="",
            gender="other",
            orientation="bisexual",
            birthdate=None,
            geohash=None,
            heat_score=0,
            is_online=False,
            date_joined=datetime.datetime.utcnow(),
            date_lastseen=datetime.datetime.utcnow(),
            is_profile_completed=False,
            is_confirmed=False,
            confirmed_on=None,
            previous_reset_token=None,
        )
        new_user.save()
        logging.debug("New user {} created".format(new_user.email))
        return new_user

    def to_dict(self) -> Dict:
        returned_dict = super().to_dict()
        returned_dict["tags"] = [t.to_dict() for t in self.get_tags()]
        returned_dict["reports"] = {"sent": [], "received": []}
        returned_dict["reports"]["sent"] = [r.to_dict() for r in self.get_reports_sent()]
        returned_dict["reports"]["received"] = [r.to_dict() for r in self.get_reports_received()]
        returned_dict["likes"] = {"sent": [], "received": []}
        returned_dict["likes"]["sent"] = [like.to_dict() for like in self.get_likes_sent()]
        returned_dict["likes"]["received"] = [like.to_dict() for like in self.get_likes_received()]
        returned_dict.pop("password")
        returned_dict.pop("previous_reset_token")
        return returned_dict

    @classmethod
    def create_table(cls):
        create_user_table(cls.db)

    def get_jwt_info(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_online": self.is_online,
            "date_lastseen": self.date_lastseen,
        }

    def get_tags(self):
        logging.debug("Getting all tags for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT tags.id as id, tags.user_id as user_id, tags.name as name
                FROM users 
                INNER JOIN tags on users.id = tags.user_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            tags = c.fetchall()
            tags_list = []
            for t in tags:
                tags_list.append(Tag(t))
        return tags_list

    def get_views(self):
        logging.debug("Getting all views for user profile {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT views.id as id, views.profile_id as profile_id, 
                views.viewer_id as viewer_id, views.dt_seen as dt_seen
                FROM users 
                INNER JOIN views on users.id = views.profile_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            views = c.fetchall()
            views_list = []
            for v in views:
                views_list.append(View(v))
        return views_list

    def get_reports_received(self):
        logging.debug("Getting all reports received for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT reports.id as id, reports.reported_id as reported_id, 
                reports.reporter_id as reporter_id, reports.dt_reported as dt_reported,
                reports.details as details, reports.reason as reason, reports.status as status
                FROM users 
                INNER JOIN reports on users.id = reports.reported_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            reports = c.fetchall()
            reports_list = []
            for r in reports:
                reports_list.append(Report(r))
        return reports_list
    def get_messages(self) -> List[Message]:
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT 
                messages.from_id as from_id, 
                messages.to_id as to_id, 
                messages.id as id, 
                messages.timestamp as timestamp, 
                messages.seen_timestamp as seen_timestamp, 
                messages.content as content, 
                messages.is_liked as is_liked, 
                messages.is_seen as is_seen
                FROM messages 
                INNER JOIN users on users.id = messages.from_id or users.id = messages.to_id 
                WHERE users.id = CAST({} AS INT)
                """.format(
                    self.id
                )
            )
            messages = c.fetchall()
            message_list = []
            for message in messages:
                message_list.append(message.Message(message))
        return message_list

    def get_messages_with_user(self, with_user_id) -> List[Message]:
        # TODO: Create a function to get latest messages only. Maybe https://stackoverflow.com/a/41095528/6350162 ?
        # Based on time or amount of messages https://stackoverflow.com/a/3799223/6350162
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT 
                messages.from_id as from_id, 
                messages.to_id as to_id, 
                messages.id as id, 
                messages.timestamp as timestamp, 
                messages.seen_timestamp as seen_timestamp, 
                messages.content as content, 
                messages.is_liked as is_liked, 
                messages.is_seen as is_seen
                FROM messages 
                WHERE from_id=CAST({0} AS INT) and to_id=CAST({1} AS INT)

                UNION ALL

                SELECT messages.from_id as from_id, 
                messages.to_id as to_id, 
                messages.id as id, 
                messages.timestamp as timestamp, 
                messages.seen_timestamp as seen_timestamp, 
                messages.content as content, 
                messages.is_liked as is_liked, 
                messages.is_seen as is_seen
                FROM messages 
                WHERE from_id=CAST({1} AS INT) and to_id=CAST({0} AS INT)
                """.format(
                    self.id, with_user_id
                )
            )
            messages = c.fetchall()
            message_list = []
            for message in messages:
                message_list.append(message.Message(message))
        return message_list

    def get_reports_sent(self):
        logging.debug("Getting all reports sent for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT reports.id as id, reports.reported_id as reported_id, 
                reports.reporter_id as reporter_id, reports.dt_reported as dt_reported,
                reports.details as details, reports.reason as reason, reports.status as status
                FROM users 
                INNER JOIN reports on users.id = reports.reporter_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            reports = c.fetchall()
            reports_list = []
            for r in reports:
                reports_list.append(Report(r))
        return reports_list
    def send_message(self, to_id, content):
        # TODO: Send notification to the other user
        Message.create(from_id=self.id, to_id=to_id, content=content)

    def get_base_info(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_online": self.is_online,
            "date_lastseen": self.date_lastseen,
        }

    def get_likes_received(self):
        logging.debug("Getting all likes received for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT likes.id as id, likes.liked_id as liked_id, 
                likes.liker_id as liker_id, likes.dt_liked as dt_liked,
                likes.is_superlike as is_superlike
                FROM users 
                INNER JOIN likes on users.id = likes.liked_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            likes = c.fetchall()
            like_list = []
            for like in likes:
                like_list.append(Like(like))
        return like_list

    def get_likes_sent(self):
        logging.debug("Getting all likes sent for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT likes.id as id, likes.liked_id as liked_id, 
                likes.liker_id as liker_id, likes.dt_liked as dt_liked,
                likes.is_superlike as is_superlike
                FROM users 
                INNER JOIN likes on users.id = likes.liker_id 
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            likes = c.fetchall()
            like_list = []
            for like in likes:
                like_list.append(Like(like))
        return like_list

    def already_likes(self, liked_id: int) -> bool:
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT EXISTS(
                  SELECT * FROM likes WHERE
                    liker_id = CAST({} AS UNSIGNED) and 
                    liked_id = CAST({} AS UNSIGNED)
                )
                """.format(
                    self.id, liked_id
                )
            )
            result = c.fetchone()
            value = next(iter(result.values()))
            return bool(value)

    def get_matches(self):
        logging.debug("Getting all matches for user {}".format(self.id))
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT matches.id as id, matches.user_1 as user_1,
                matches.user_2 as user_2, matches.dt_matched as dt_matched
                FROM users
                INNER JOIN matches on users.id = matches.user_1 or users.id = matches.user_2
                WHERE users.id = CAST({} AS UNSIGNED)
                """.format(
                    self.id
                )
            )
            matches = c.fetchall()
            match_list = []
            for match in matches:
                match_list.append(Match(match))
        return match_list


def get_user(uid: Any[int, str]) -> Optional[User]:
    not_found = 0
    # These initializations are to make PEP happy and silence warnings
    f_user = None

    if isinstance(uid, str):
        uid = uid.lower()

    try:
        user = User.get(id=uid)
    except ValueError:
        not_found += 1
    else:
        f_user = user
    try:
        user = User.get(username=uid)
    except ValueError:
        not_found += 1
    else:
        f_user = user
    try:
        user = User.get(email=uid)
    except ValueError:
        not_found += 1
    else:
        f_user = user
    # If none of those worked, throw an error
    if not_found == 3:
        logging.debug("User {} not found.".format(uid))
        raise NotFoundError("User {} not found.".format(uid), "Try again with another uid")
    logging.debug("Found user {} from {}".format(f_user.id, uid))
    return f_user
