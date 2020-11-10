"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/gmorer
    <jlasne@student.42.fr> - <lauris.skraucis@gmail.com>

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
import os

from PyMatcha import application
from PyMatcha.utils.logging import setup_logging

if __name__ == "__main__":
    # Get the port defined in env if defined, otherwise sets it to 5000
    port = int(os.environ.get("FLASK_PORT", "5000"))
    # Default debug is true
    debug = bool(os.environ.get("FLASK_DEBUG", False))

    setup_logging()

    # Runs the main loop
    application.run(host=os.getenv("FLASK_HOST", "0.0.0.0"), port=port, debug=debug)
