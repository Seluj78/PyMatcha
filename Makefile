VENV = $(PWD)/venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest


all: build
	# TODO: Build and run the server

install:
	test -d $(VENV) || python3 -m venv $(VENV)
	# TODO: Create envs, install everything

build: install
	# TODO: Run the build process for frontend

backend: build
	# TODO: Run the backend server in standalone

frontend: build
	# TODO: Run the frontend server in standalone

prod: build
	# TODO: Run the whole server for prod

dev: build
	# TODO: Run the whole server for dev

tests: build
	# TODO: Run the tests

clean:
	rm -rf frontend/build

re: clean all

.PHONY : build backend frontend prod dev clean tests fclean all re