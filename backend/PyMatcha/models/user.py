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

import datetime
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import Geohash
from PyMatcha.models.image import Image
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.message import Message
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
            logging.warning("Email {} taken".format(email))
            raise ConflictError("Email {} taken.".format(email), "Use another email.")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            logging.warning("Username {} taken".format(username))
            raise ConflictError("Username {} taken.".format(username), "Try another username.")

        # Check correct gender
        if gender not in ["male", "female", "other"]:
            logging.warning("Gender must be male, female or other, not {}".format(gender))
            raise ConflictError("Gender must be male, female or other, not {}.".format(gender))

        # Check correct orientation
        if orientation not in ["heterosexual", "homosexual", "bisexual", "other"]:
            logging.warning(
                "Sexual Orientation must be heterosexual, homosexual, bisexual or other, not {}.".format(orientation)
            )
            raise ConflictError(
                "Sexual Orientation must be heterosexual, homosexual, bisexual or other, not {}.".format(orientation)
            )

        # Check correct geohash
        try:
            Geohash.decode(geohash)
        except ValueError as e:
            logging.warning("Geohash error: {}".format(e))
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
            raise ConflictError("Email {} taken.".format(email), "Use another email.")

        # Check username availability
        try:
            User.get(username=username)
        except ValueError:
            pass
        else:
            logging.warning("Username {} taken".format(username))
            raise ConflictError("Username {} taken.".format(username), "Try another username.")

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
        returned_dict["images"] = [image.to_dict() for image in self.get_images()]
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

    def get_images(self):
        logging.debug("Getting all images for user {}".format(self.id))
        image_list = Image.get_multis(user_id=self.id)
        if not image_list:
            return []
        else:
            return image_list

    def get_tags(self):
        logging.debug("Getting all tags for user {}".format(self.id))
        tag_list = Tag.get_multis(user_id=self.id)
        if not tag_list:
            return []
        else:
            return tag_list

    def get_views(self):
        logging.debug("Getting all views for user profile {}".format(self.id))
        view_list = View.get_multis(profile_id=self.id)
        if not view_list:
            return []
        else:
            return view_list

    def get_reports_received(self):
        logging.debug("Getting all reports received for user {}".format(self.id))
        reports_received_list = Report.get_multis(reported_id=self.id)
        if not reports_received_list:
            return []
        else:
            return reports_received_list

    def get_reports_sent(self):
        logging.debug("Getting all reports sent for user {}".format(self.id))
        reports_sent_list = Report.get_multis(reporter_id=self.id)
        if not reports_sent_list:
            return []
        else:
            return reports_sent_list

    def get_likes_received(self):
        logging.debug("Getting all likes received for user {}".format(self.id))
        likes_received_list = Like.get_multis(liked_id=self.id)
        if not likes_received_list:
            return []
        else:
            return likes_received_list

    def get_likes_sent(self):
        logging.debug("Getting all likes sent for user {}".format(self.id))
        likes_sent_list = Like.get_multis(liker_id=self.id)
        if not likes_sent_list:
            return []
        else:
            return likes_sent_list

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

    def send_message(self, to_id, content):
        Message.create(from_id=self.id, to_id=to_id, content=content)

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
                WHERE users.id = CAST({} AS SIGNED)
                """.format(
                    self.id
                )
            )
            messages = c.fetchall()
            message_list = []
            for message in messages:
                message_list.append(Message(message))
        logging.debug("Getting all messages sent or received by user {}".format(self.id))
        return message_list

    def get_conversation_list(self) -> List[Message]:
        with self.db.cursor() as c:
            c.execute(
                """
                SELECT t1.*
                FROM messages AS t1
                INNER JOIN
                (
                    SELECT
                        LEAST(from_id, to_id) AS from_id,
                        GREATEST(from_id, to_id) AS to_id,
                        MAX(id) AS max_id
                    FROM messages
                    GROUP BY
                        LEAST(from_id, to_id),
                        GREATEST(from_id, to_id)
                ) AS t2
                    ON LEAST(t1.from_id, t1.to_id) = t2.from_id AND
                       GREATEST(t1.from_id, t1.to_id) = t2.to_id AND
                       t1.id = t2.max_id
                    WHERE t1.from_id = {0} OR t1.to_id = {0}
                """.format(
                    self.id
                )
            )
            conversations = c.fetchall()
            conversation_list = []
            for last_message in conversations:
                conversation_list.append(Message(last_message))
        return conversation_list

    def get_messages_with_user(self, with_user_id) -> List[Message]:
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
                WHERE from_id=CAST({0} AS SIGNED) and to_id=CAST({1} AS SIGNED)

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
                WHERE from_id=CAST({1} AS SIGNED) and to_id=CAST({0} AS SIGNED)
                """.format(
                    self.id, with_user_id
                )
            )
            messages = c.fetchall()
            message_list = []
            for message in messages:
                message_list.append(Message(message))
        logging.debug(
            "Getting all messages between user {} and {} (Total: {})".format(self.id, with_user_id, len(message_list))
        )
        return message_list


def get_user(uid: Any[int, str]) -> Optional[User]:
    # These initializations are to make PEP happy and silence warnings
    f_user = None  # noqa

    if isinstance(uid, str):
        uid = uid.lower()

    try:
        uid = int(uid)
    except ValueError:
        try:
            user = User.get(username=uid)
        except ValueError:
            pass
        else:
            logging.debug("Found user {} from {}".format(user.id, uid))
            return user
        try:
            user = User.get(email=uid)
        except ValueError:
            pass
        else:
            logging.debug("Found user {} from {}".format(user.id, uid))
            return user
    else:
        try:
            user = User.get(id=uid)
        except ValueError:
            pass
        else:
            logging.debug("Found user {} from {}".format(user.id, uid))
            return user
    # If none of those worked, throw an error
    logging.debug("User {} not found.".format(uid))
    raise NotFoundError("User {} not found.".format(uid))
