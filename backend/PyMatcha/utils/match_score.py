from typing import List

from fuzzywuzzy import fuzz
from Geohash import decode
from geopy.distance import distance


def _get_distance(geohash_1: str, geohash_2: str) -> float:
    coords_1 = decode(geohash_1)
    coords_2 = decode(geohash_2)
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


def _get_inverted_gender(gender, orientation):
    # TODO: Handle other gender and bisexual and other orientations
    if orientation == "heterosexual":
        return "male" if gender == "female" else "female"
    elif orientation == "homosexual":
        return "male" if gender == "male" else "female"
    else:
        return "other"
