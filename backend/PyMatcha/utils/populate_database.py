import datetime
import json
import os
import random

import Geohash
import lorem
from PyMatcha.models.image import Image
from PyMatcha.models.tag import Tag
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.utils.errors import ConflictError
from randomuser import RandomUser


def gen_datetime(min_year: int = 1900, max_year: int = datetime.datetime.now().year) -> datetime.datetime:
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + datetime.timedelta(days=365 * years)
    return start + (end - start) * random.random()


def populate_users(amount=150, drop_user_table=False):
    if drop_user_table:
        User.drop_table()
        User.create_table()
    users = RandomUser.generate_users(amount=amount)
    for user in users:
        gender = random.choice(["male", "female", "other"])
        if gender != "other":
            if gender == user.get_gender():
                pass
            else:
                gender = user.get_gender()
        orientation = random.choice(["heterosexual", "homosexual", "bisexual", "other"])

        bio = lorem.paragraph()

        coords = user.get_coordinates()
        geohash = Geohash.encode(float(coords["latitude"]), float(coords["longitude"]))

        date_joined = gen_datetime(min_year=2017, max_year=datetime.datetime.now().year)

        date_lastseen = gen_datetime(min_year=2017, max_year=datetime.datetime.now().year)
        username = user.get_username()

        birthdate = gen_datetime(min_year=1985, max_year=datetime.datetime.now().year - 18).date()
        try:
            User.create(
                first_name=user.get_first_name(),
                last_name=user.get_last_name(),
                email=user.get_email(),
                username=username,
                password=user.get_password(),
                bio=bio,
                gender=gender,
                orientation=orientation,
                birthdate=birthdate,
                geohash=geohash,
                heat_score=0,
                is_online=random.choice([True, False]),
                date_joined=date_joined,
                date_lastseen=date_lastseen,
                is_profile_completed=True,
                is_confirmed=True,
                confirmed_on=datetime.datetime.utcnow(),
            )
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(dir_path + "/tags.json") as handle:
                json_list = json.load(handle)
            u = get_user(username)
            tags = list(set(random.sample(json_list, 8)))

            for tag in tags:
                Tag.create(name=tag, user_id=u.id)
            Image.create(user_id=u.id, link=user.get_picture(), is_primary=True)
        except ConflictError:
            pass  # Pass on the conflict error, this user wont be created because the username is taken. Who cares ?


if __name__ == "__main__":
    populate_users()
