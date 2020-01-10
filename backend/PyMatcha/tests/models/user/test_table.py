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


from PyMatcha.models.user import User


class TestFixturesViewAdmin:
    def test_is_user_table_exists(self):
        assert User.table_exists()

    def test_is_user_table_empty(self):
        assert User.select().count() == 0

    def test_create_tmp_user(self):
        User.create(username="tmp", first_name="tmp", last_name="tmp", email="tmp.tmp@tmp.tmp").save()
        assert User.select().count() == 1

    def test_delete_tmp_user(self):
        User.delete_by_id(1)
        assert User.select().count() == 0
