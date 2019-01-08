# coding=utf-8

"""
    PyMatcha - A Python Dating Website
    Copyright (C) 2018-2019 jlasne/ynacache
    <jlasne@student.42.fr> - <ynacache@student.42.fr>

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
#!/bin/bash

source venv/bin/activate

export FLASK_DEBUG=1
export FLASK_SECRET_KEY="ThisIsADevelopmentKey"
export FLASK_ADMIN_SWATCH="simplex"
export DB_USER=pymatcharoot
export DB_PASSWORD=KyCeX74azyKH
export DB_HOST=pymatchadb.cvesmjtn6kz7.eu-west-3.rds.amazonaws.com

python app.py runserver