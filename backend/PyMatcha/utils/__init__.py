from PyMatcha.utils.password import hash_password
from PyMatcha.utils.tables import _create_likes_table
from PyMatcha.utils.tables import _create_reports_table
from PyMatcha.utils.tables import _create_tags_table
from PyMatcha.utils.tables import _create_user_images_table
from PyMatcha.utils.tables import _create_user_table
from PyMatcha.utils.tables import _create_views_table
from PyMatcha.utils.tables import create_tables

create_user_images_table = _create_user_images_table
create_user_table = _create_user_table
create_tags_table = _create_tags_table
create_views_table = _create_views_table
create_reports_table = _create_reports_table
create_likes_table = _create_likes_table

__all__ = [
    "hash_password",
    "create_tables",
    "create_user_table",
    "create_user_images_table",
    "create_tags_table",
    "create_views_table",
    "create_reports_table",
    "create_likes_table",
]
