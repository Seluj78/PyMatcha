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


import pytest

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from flask import url_for


class TestLiveServer:
    def test_server_is_alive(self, live_server):
        assert live_server._process
        assert live_server._process.is_alive()

    def test_server_url(self, live_server):
        assert live_server.url() == "http://localhost:%d" % live_server.port
        assert live_server.url("/ping") == "http://localhost:%d/ping" % live_server.port

    def test_server_listening(self, live_server):
        res = urlopen(live_server.url("/ping"))
        assert res.code == 200
        assert b"pong" in res.read()

    def test_url_for(self, live_server):
        assert url_for("ping_pong.ping", _external=True) == "http://localhost:%s/ping" % live_server.port

    def test_set_application_server_name(self, live_server):
        assert live_server.app.config["SERVER_NAME"] == "localhost:%d" % live_server.port

    @pytest.mark.options(server_name="example.com:5000")
    def test_rewrite_application_server_name(self, live_server):
        assert live_server.app.config["SERVER_NAME"] == "example.com:%d" % live_server.port
