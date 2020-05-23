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
DOCKER_NAME := pymatcha
FLASK_PORT := 5000

all: install build run

install_python:
ifndef TRAVIS
		test -d $(VENV) || python -m venv $(VENV)
		( \
			source $(VENV)/bin/activate; \
			pip install wheel; \
			$(PIP) install -r $(BACKEND)/requirements.txt \
		)
endif

install_react:
	npm install --prefix $(FRONTEND)

install: install_python install_react

docker_build: install_react
	mkdir -p www
	mkdir -p www/frontend
	mkdir -p www/backend

	npm run build --prefix $(FRONTEND)
	cp -R $(FRONTEND)/build www/frontend

	# TODO: Add obfuscation/compilation step
	cp -R $(BACKEND) www/

build: install
	mkdir -p www
	mkdir -p www/frontend
	mkdir -p www/backend

	npm run build --prefix $(FRONTEND)
	cp -R $(FRONTEND)/build www/frontend

	# TODO: Add obfuscation/compilation step
	cp -R $(BACKEND) www/

dev: install
	npm run start --prefix $(FRONTEND) &
	# TODO: Run the whole server for dev

run: build
	( \
		source .env; \
		source $(VENV)/bin/activate && \
		python3 $(BACKEND)/app.py \
	)
	# TODO: Run the whole server for prod

lint:
ifdef TRAVIS
	flake8 backend/
	black --check backend/
else
	( \
		source $(VENV)/bin/activate && \
		$(PIP) install -r $(BACKEND)/requirements-dev.txt && \
		flake8 backend/ && \
		black --check backend/ \
	)
endif


tests: build
ifdef TRAVIS
	pytest backend/
else
	( \
		test -d frontend/build && \
		source $(VENV)/bin/activate && \
		$(PIP) install -r $(BACKEND)/requirements-dev.txt && \
		pytest backend/ \
	)
endif
	# TODO: Maybe move this to the build stage? so if the build fails and the folder isn't here it fails immediatly and not at the test stage


# TODO Update makefile for docker compose
docker: build docker-build docker-run

docker-run:
	docker run --name $(DOCKER_NAME) --restart=always -p 8080:$(FLASK_PORT) -d $(DOCKER_NAME)

docker-build:
	-docker kill $(DOCKER_NAME)
	docker build -t $(DOCKER_NAME) .

docker-clean:
	-docker kill $(DOCKER_NAME)
	-docker ps -a | awk '{ print $$1,$$2 }' | grep $(DOCKER_NAME) | awk '{print $$1 }' | xargs -I {} docker rm {}
	docker image rm $(DOCKER_NAME)

clean:
	rm -rf $(FRONTEND)/node_modules
	rm -rf $(VENV)

fclean: clean docker-clean
	rm -rf $(FRONTEND)/build
	rm -rf $(VENV)
	rm -rf www

re: clean all

.PHONY : all install_python install_react install build dev run tests docker clean fclean re docker docker-build docker-clean docker-run
