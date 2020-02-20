import lorem
import names
import string
import random
import Geohash
import datetime

from PyMatcha.models import User


def gen_datetime(min_year=1900, max_year=datetime.datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime.datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + datetime.timedelta(days=365 * years)
    return start + (end - start) * random.random()


def populate_users():
    User.drop_table()
    User.create_table()
    for i in range(0, 500):
        gender = random.choice(["male", "female", "other"])

        orientation = random.choice(["heterosexual", "homosexual", "bisexual"])

        first_name = names.get_first_name(gender=gender if gender != "other" else None)

        last_name = names.get_last_name()

        username = first_name + last_name  # TODO: More randomness in usernames

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
        User.create(
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
            tags="",  # TODO: Change to a real random tag generation
            heat_score=0,
            online=random.choice([True, False]),
            date_joined=date_joined,
            date_lastseen=date_lastseen,
            deleted=False,
        )
    # TODO: Add images


if __name__ == "__main__":
    populate_users()
