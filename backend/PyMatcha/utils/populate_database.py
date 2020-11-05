import datetime
import json
import os
import random
from time import sleep
from urllib.error import HTTPError

import Geohash
import lorem
import requests
from PyMatcha.models.image import Image
from PyMatcha.models.tag import Tag
from PyMatcha.models.user import get_user
from PyMatcha.models.user import User
from PyMatcha.utils.errors import ConflictError
from randomuser import RandomUser
from tqdm import tqdm

FRANCE_GEOHASH_START = ("u0", "gb", "ez", "sp")
NATIONALITIES_PARAMS = {"nat": "fr"}

# LATVIA_GEOHASH_START = ("d0", "d1", "d4", "d4")
# NATIONALITIES_PARAMS = {"nat": "lv"}


def gen_datetime(min_year: int = 1900, max_year: int = datetime.datetime.now().year) -> datetime.datetime:
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + datetime.timedelta(days=365 * years)
    return start + (end - start) * random.random()


def get_unsplash_image(gender):
    link = None
    while True:
        r = requests.get(f"https://source.unsplash.com/featured/?{gender}")
        if r.status_code == 403:
            sleep(1)
            continue
        link = r.url
        if not Image.get(link=link):
            break
    return link


def populate_users(amount=150, drop_user_table=False):
    if drop_user_table:
        User.drop_table()
        User.create_table()
    try:
        users = RandomUser.generate_users(amount=amount, get_params=NATIONALITIES_PARAMS)
    except HTTPError:
        sleep(10)
        users = RandomUser.generate_users(amount=amount, get_params=NATIONALITIES_PARAMS)
    for user in tqdm(users):
        gender = random.choice(["male", "female", "other"])
        if gender != "other":
            if gender == user.get_gender():
                pass
            else:
                gender = user.get_gender()
        orientation = random.choice(["heterosexual", "homosexual", "bisexual", "other"])

        bio = lorem.paragraph()

        coords = user.get_coordinates()
        geohash = str(Geohash.encode(float(coords["latitude"]), float(coords["longitude"])))
        if not geohash.startswith(FRANCE_GEOHASH_START):
            old = geohash[0:2]
            geohash = geohash.replace(old, FRANCE_GEOHASH_START[0], 1)

        dt_joined = gen_datetime(min_year=2017, max_year=datetime.datetime.now().year)

        dt_lastseen = gen_datetime(min_year=2017, max_year=datetime.datetime.now().year)
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
                heat_score=random.randint(0, 150),
                is_online=random.choice([True, False]),
                dt_joined=dt_joined,
                dt_lastseen=dt_lastseen,
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

            if gender == "other":
                # Change the gender because the profile picture needs to be of a person
                gender = random.choice(["male", "female"])
            image_url = get_unsplash_image("man" if gender == "male" else "woman")
            if not image_url:
                raise ValueError("ERROR ON GETTING IMAGE FROM UNSPLASH")

            Image.create(user_id=u.id, link=image_url, is_primary=True)
        except ConflictError:
            pass  # Pass on the conflict error, this user wont be created because the username is taken. Who cares ?


if __name__ == "__main__":
    populate_users()
