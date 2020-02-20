from PyMatcha.utils.password import hash_password
from PyMatcha.utils.tables import create_tables, _create_user_images_table, _create_user_table

create_user_images_table = _create_user_images_table
create_user_table = _create_user_table

__all__ = ["hash_password", "create_tables", "create_user_table", "create_user_images_table"]
