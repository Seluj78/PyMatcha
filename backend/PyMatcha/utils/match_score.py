import itertools
from typing import List
from typing import Optional

from fuzzywuzzy import fuzz
from Geohash import decode
from geopy.distance import distance
from PyMatcha.models.user import User


def _get_distance(geohash_1: str, geohash_2: str) -> Optional[float]:
    try:
        coords_1 = decode(geohash_1)
        coords_2 = decode(geohash_2)
    except TypeError:
        return None
    else:
        return distance(coords_1, coords_2).kilometers


def _get_common_tags(tag_list_1: list, tag_list_2: list) -> List[str]:
    """Will return the list of common tags
    """
    common_tags = []
    for tag_1 in tag_list_1:
        for tag_2 in tag_list_2:
            if fuzz.partial_ratio(tag_1, tag_2) >= 70:
                common_tags.append(tag_1 if len(tag_1) > len(tag_2) else tag_2)
    return list(set(common_tags))


def _get_age_diff(age_1: int, age_2: int) -> int:
    return -1 * (age_1 - age_2)


def _get_gender_query(orientation, gender):
    if orientation == "heterosexual":
        if gender == "female":
            q1 = User.get_multis(orientation=orientation, gender="male")
            q2 = User.get_multis(orientation="other", gender="male")
            q1.extend(q2)
            return q1
        elif gender == "male":
            q1 = User.get_multis(orientation=orientation, gender="female")
            q2 = User.get_multis(orientation="other", gender="female")
            q1.extend(q2)
            return q1
        else:
            q1 = User.get_multis(orientation=orientation, gender="female")
            q2 = User.get_multis(orientation=orientation, gender="male")
            q1.extend(q2)
            return q1
    elif orientation == "homosexual":
        if gender == "female":
            q1 = User.get_multis(orientation=orientation, gender="female")
            q2 = User.get_multis(orientation="other", gender="female")
            q1.extend(q2)
            return q1
        elif gender == "male":
            q1 = User.get_multis(orientation=orientation, gender="male")
            q2 = User.get_multis(orientation="other", gender="male")
            q1.extend(q2)
            return q1
        else:
            q1 = User.get_multis(orientation=orientation, gender="female")
            q2 = User.get_multis(orientation=orientation, gender="male")
            q1.extend(q2)
            return q1
    elif orientation == "bisexual":
        q1 = User.get_multis(orientation=orientation, gender="female")
        q3 = User.get_multis(orientation=orientation, gender="male")
        q2 = []
        q4 = []
        if gender == "female":
            q2 = User.get_multis(orientation="homosexual", gender="female")
        if gender == "male":
            q4 = User.get_multis(orientation="homosexual", gender="male")
        q5 = User.get_multis(orientation="other", gender="male")
        q6 = User.get_multis(orientation="other", gender="female")
        return list(set(list(itertools.chain(q1, q2, q3, q4, q5, q6))))
    elif orientation == "other":
        q1 = User.get_multis(orientation=orientation, gender="female")
        q3 = User.get_multis(orientation=orientation, gender="male")
        q2 = []
        q4 = []
        q5 = []
        q6 = []
        if gender == "female":
            q2 = User.get_multis(orientation="homosexual", gender="female")
            q5 = User.get_multis(orientation="heterosexual", gender="male")
        if gender == "male":
            q4 = User.get_multis(orientation="homosexual", gender="male")
            q6 = User.get_multis(orientation="heterosexual", gender="female")
        return list(set(list(itertools.chain(q1, q2, q3, q4, q5, q6))))
    else:
        raise ValueError("No match found for genre. This should not happen")
