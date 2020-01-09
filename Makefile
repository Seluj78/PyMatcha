SHELL := /bin/bash
VENV = $(PWD)/venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest
FRONTEND = $(PWD)/frontend
BACKEND = $(PWD)/backend

all: install build prod
	# TODO: Build and run the server

install_python:
	test -d $(VENV) || python3.7 -m venv $(VENV)
	( \
		source $(VENV)/bin/activate; \
		$(PIP) install -r $(BACKEND)/requirements.txt \
	)
	# TODO: Create envs, install everything

install_react:
	npm install --prefix $(FRONTEND)

install: install_python install_react

build: install_react
	npm run build --prefix $(FRONTEND)

dev: install
	npm run start --prefix $(FRONTEND) &
	# TODO: Run the whole server for dev

prod: install build
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
