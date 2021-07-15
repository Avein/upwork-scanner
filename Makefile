SHELL=/bin/bash

VENV_NAME=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin
PYTHON=${VENV_BIN}/python3

DOCKER_IMAGE="argyle-task"
GIT_HASH=$(shell git rev-parse --short HEAD)

.DEFAULT_GOAL := help

help:
	@echo "Available Makefile targets:"
	@echo "* venv"
	@echo "    Create virtualenv and install dependencies"
	@echo "* clean"
	@echo "    Remove all generated files"
	@echo "* lint"
	@echo "    Run python tools to check source code (mypy, isort, black, flake8)"
	@echo "* run_job"
	@echo "    Start default job"
	@echo "* docker"
	@echo "    Build docker image"
	@echo "* docker_run"
	@echo "    Run built docker image"
	@echo "* hook"
	@echo "    Install pre-commit hook"
	@echo "* hook_uninstall"
	@echo "    Uninstall pre-commit hook"

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt dev-requirements.txt
	@echo "***** Checking virtualenv..."
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)
	@echo "***** Updating pip..."
	${PYTHON} -m pip install -U pip
	@echo "***** Updating dependencies..."
	${PYTHON} -m pip install -r dev-requirements.txt
	touch $(VENV_NAME)/bin/activate

clean:
	rm -rf $(VENV_NAME) __pycache__ .mypy_cache

lint: venv
	@echo "***** Running mypy"
	${PYTHON} -m mypy ./src
	@echo "***** Running isort"
	${PYTHON} -m isort ./src
	@echo "***** Running black"
	${PYTHON} -m black ./src
	@echo "***** Running flake8"
	${PYTHON} -m flake8 ./src

docker:
	docker build -t ${DOCKER_IMAGE}:${GIT_HASH} .

docker_run:
	docker run -v /$(shell pwd)/src/results/:/code/results/ ${DOCKER_IMAGE}:${GIT_HASH}

run_job: venv
	cd src && ${PYTHON} job.py

hook: venv
	pre-commit install

hook_uninstall: venv
	pre-commit uninstall
