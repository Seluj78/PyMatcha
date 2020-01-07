VENV = $(PWD)/venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python
FLASK = $(VENV)/bin/flask
PYTEST = $(VENV)/bin/pytest
FRONTEND = $(PWD)/frontend
BACKEND = $(PWD)/frontend

all: build
	# TODO: Build and run the server

install:
	# TODO: Separate python and nodejs install rules
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install -r $(BACKEND)/requirements.txt
	cd $(FRONTEND); npm install
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
	pip install -r $(BACKEND)/requirements-dev.txt
	# TODO: Run the tests

clean:
	rm -rf $(FRONTEND)/build
	rm -rf $(FRONTEND)/node_modules

re: clean all

.PHONY : build backend frontend prod dev clean tests fclean all re