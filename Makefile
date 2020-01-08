SHELL := /bin/bash
VENV = $(PWD)/venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest
FRONTEND = $(PWD)/frontend
BACKEND = $(PWD)/backend

all: build
	# TODO: Build and run the server

install:
	# TODO: Separate python and nodejs install rules
	test -d $(VENV) || python3.7 -m venv $(VENV)
	( \
		source $(VENV)/bin/activate; \
		$(PIP) install -r $(BACKEND)/requirements.txt \
	)
	npm install --prefix $(FRONTEND)
	# TODO: Create envs, install everything

build: install
	npm run build --prefix $(FRONTEND)

dev: install
	npm run start --prefix $(FRONTEND) &
	# TODO: Run the whole server for dev

prod: build
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
	( \
		source $(VENV)/bin/activate; \
		$(PIP) install -r $(BACKEND)/requirements-dev.txt \
	)
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
