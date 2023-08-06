.PHONY: clean clean-test clean-pyc clean-build help lint black test \
	test-all dist install install-dev uninstall tags 
.DEFAULT_GOAL := help

COVERAGE= --cov=tlsmate_client_simul
PYTEST_SUBPROCESS=$(shell pip show pytest-xdist 2&> /dev/null && echo "-n auto")

SHELL := /bin/bash

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, docs and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 tlsmate_client_simul tests

black: ## check if black would reformat the python code
	black --check tlsmate_client_simul tests

black-diff: ## provide the changes black would do as a diff
	black --check --diff tlsmate_client_simul tests

black-reformat: ## let black reformat the python code
	black tlsmate_client_simul tests

test: ## run tests quickly with the default Python
	py.test $(PYTEST_SUBPROCESS)

test-cov: ## generate coverage statistics
	py.test $(COVERAGE) $(PYTEST_SUBPROCESS)

test-cov-report: ## generate coverage report for each file
	py.test --cov-report annotate:cov_annotate $(COVERAGE) $(PYTEST_SUBPROCESS)

test-all: ## run tests on every Python version with tox
	tox

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: ## install the package using pip
	pip install .

install-dev: ## install the package using the development environment
	pip install -e .[dev]

uninstall: ## uninstall the package using pip
	pip uninstall tlsmate_client_simul
