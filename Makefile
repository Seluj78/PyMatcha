#    PyMatcha - A Python Dating Website
#    Copyright (C) 2018-2019 jlasne/gmorer
#    <jlasne@student.42.fr> - <gmorer@student.42.fr>
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


SHELL := /bin/bash
VENV = $(PWD)/venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest
FRONTEND = $(PWD)/frontend
BACKEND = $(PWD)/backend

all: install build run
	# TODO: Build and run the server

install_python:
ifndef TRAVIS
		test -d $(VENV) || python3.7 -m venv $(VENV)
		( \
			source $(VENV)/bin/activate; \
			pip install wheel; \
			$(PIP) install -r $(BACKEND)/requirements.txt \
		)
endif
	# TODO: Create envs, install everything

install_react:
	npm install --prefix $(FRONTEND)

install: install_python install_react

build: install
	# TODO: add test -d or something similar to ignore or update existing files
	mkdir www
	mkdir www/frontend
	mkdir www/backend

	npm run build --prefix $(FRONTEND)
	cp -R $(FRONTEND)/build www/frontend

	# TODO: Add obfuscation/compilation step
	cp -R $(BACKEND) www/

dev: install
	npm run start --prefix $(FRONTEND) &
	# TODO: Run the whole server for dev

run: build
	( \
		export DB_USER=EWARSESTHJ; \
		export DB_PASSWORD=EWARSESTHJ; \
		export FLASK_SECRET_KEY=EWARSESTHJ; \
		export FLASK_DEBUG=EWARSESTHJ; \
		source $(VENV)/bin/activate && \
		python3 $(BACKEND)/app.py \
	)
	# TODO: Run the whole server for prod

tests: build
	test -d frontend/build
	# TODO: Maybe move this to the build stage? so if the build fails and the folder isn't here it fails immediatly and not at the test stage
	# TODO: Run the tests

docker: build
	docker build -t pymatcha:latest .

clean:
	rm -rf $(FRONTEND)/node_modules
	rm -rf $(VENV)

fclean: clean
	rm -rf $(FRONTEND)/build
	rm -rf $(VENV)
	rm -rf www

re: clean all

.PHONY : all install_python install_react install build dev run tests docker clean fclean re
