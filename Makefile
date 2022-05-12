MAJOR_VERSION = 1
MINOR_VERSION = 0
BUILD_NUMBER ?= 6
artifacts = ./artifacts
pkg_name = pythonbot

VERSION := $(MAJOR_VERSION).$(MINOR_VERSION).$(BUILD_NUMBER)

.PHONY: all
all: build lint test

.PHONY: check-env
check-env:
	@echo Checking environment ...
	pipenv --version

.PHONY: setup
setup:
	pipenv update --dev

.PHONY: lint
lint: setup
	pipenv run flake8 --verbose

.PHONY: build
build: check-env clean lint

.PHONY: shell
shell:
	PYTHONPATH=$(shell pwd) pipenv shell

.PHONY: test
test:
	pipenv run pytest --verbose --color=yes

.PHONY: coverage
coverage:
	pipenv run coverage run -m --include="pythonbot/*" --omit="/" pytest --verbose --color=yes
	pipenv run coverage report -m --include="pythonbot/*"

.PHONY: clean
clean:
	@echo Cleaning environment ...
	# may not be a venv to remove, but just keep going in that case
	pipenv --rm || true
	rm -rf *.egg-info build dist .coverage Pipfile.lock
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +

.PHONY: package
package: clean setup
	@echo Packaging application ...
	@echo Version: $(VERSION)
	mkdir -p build
	pipenv lock -r > build/requirements.txt
	VERSION=$(VERSION) \
		pipenv run python setup.py bdist_wheel
