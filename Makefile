SHELL := /bin/bash
VENV = $(PWD)/venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest
FRONTEND = $(PWD)/frontend
BACKEND = $(PWD)/backend

all: build
	# TODO: Build and run the server

install:
	# TODO: Separate python and nodejs install rules
	test -d $(VENV) || python3 -m venv $(VENV)
	source $(VENV)/bin/activate
	$(PIP) install -r $(BACKEND)/requirements.txt
	npm run install --prefix $(FRONTEND)
	# TODO: Create envs, install everything

build: install
	npm run build --prefix $(FRONTEND)

dev: install
	npm run start --prefix $(FRONTEND) &
	# TODO: Run the whole server for dev

prod: build
	# TODO: Run the whole server for prod

tests: build
	pip install -r $(BACKEND)/requirements-dev.txt
	# TODO: Run the tests

docker:
	# TODO

clean:
	rm -rf $(FRONTEND)/node_modules

fclean: clean
	rm -rf $(FRONTEND)/build
	rm -rf $(VENV)

re: clean all

.PHONY : build backend frontend prod dev clean tests fclean all re