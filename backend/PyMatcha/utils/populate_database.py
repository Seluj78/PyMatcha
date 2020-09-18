import datetime
import json
import os
import random
import string

import Geohash
import lorem
import names
from PyMatcha.models.tag import Tag
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.utils.errors import ConflictError


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
    for i in range(0, amount):
        gender = random.choice(["male", "female", "other"])

        orientation = random.choice(["heterosexual", "homosexual", "bisexual", "other"])

        first_name = names.get_first_name(gender=gender if gender != "other" else None)

        last_name = names.get_last_name()

        password_size = random.randint(6, 14)
        chars = string.printable
        password = "".join(random.choice(chars) for i in range(password_size))

        bio = lorem.paragraph()

        birthdate = gen_datetime(min_year=1960, max_year=datetime.datetime.now().year - 18)

        lat = random.random() * 2.0
        lng = random.random() * 2.0
        geohash = Geohash.encode(lat, lng)

        date_joined = gen_datetime(min_year=2017, max_year=datetime.datetime.now().year)

        date_lastseen = gen_datetime(min_year=2017, max_year=datetime.datetime.now().year)

        middle_mail = random.choice([".", "", "_"])
        number = str(random.randint(0, 999))
        end_mail = random.choice(["", number])
        email = first_name + middle_mail + last_name + end_mail + "@gmail.com"

        end_of_username = random.choice(["", number, last_name])

        username = first_name + end_of_username

        try:
            User.create(
                first_name=first_name,
                last_name=last_name,
                email=email.lower(),
                username=username,
                password=password,
                bio=bio,
                gender=gender,
                orientation=orientation,
                birthdate=birthdate.date(),
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
        except ConflictError:
            pass  # Pass on the conflict error, this user wont be created because the username is taken. Who cares ?


if __name__ == "__main__":
    populate_users()
