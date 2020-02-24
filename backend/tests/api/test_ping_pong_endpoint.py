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


# import pytest

from flask import url_for


class TestPingPongJSONResponse:
    def test_json_response(self, client, accept_json):
        res = client.get(url_for("ping_pong.ping"), headers=accept_json)
        assert res.json == {"ping": "pong"}

    def test_json_response_compare_to_status_code(self, client, accept_json):
        assert client.get(url_for("ping_pong.ping"), headers=accept_json) == 200
        # assert client.get("fake-route", headers=accept_json) == 404
        # assert client.get("fake-route", headers=accept_json) != "404"
        # res = client.get(url_for("ping_pong.ping"), headers=accept_json)
        # assert res == res

    def test_mismatching_eq_comparison(self, client, accept_json):
        # with pytest.raises(AssertionError, match=r"Mismatch in status code"):
        #     assert client.get("fake-route", headers=accept_json) == 200
        # with pytest.raises(AssertionError, match=r"404 NOT FOUND"):
        #     assert client.get("fake-route", headers=accept_json) == "200"
        pass

    def test_dont_rewrite_existing_implementation(self, app, accept_json):
        class MyResponse(app.response_class):
            @property
            def json(self):
                # What is the meaning of life, the universe and everything?
                return 42

        app.response_class = MyResponse
        client = app.test_client()

        res = client.get(url_for("ping_pong.ping"), headers=accept_json)
        assert res.json == 42
