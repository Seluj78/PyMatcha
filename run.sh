#!/bin/bash

#    PyMatcha - A Python Dating Website
#    Copyright (C) 2018-2019 jlasne/nbeny
#    <jlasne@student.42.fr> - <nbeny@student.42.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

echo "Do not run this as a production server!"

export FLASK_ENV='dev'
export FLASK_DEBUG=1
export FLASK_SECRET_KEY="NotSoSecretKey"

source venv/bin/activate && python3 app.py