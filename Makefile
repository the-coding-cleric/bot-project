WHL_VERSION ?= patch
DOCKER_IMG ?= pythonbot:test
docker_workdir = /workspace

.PHONY: docker_build
docker_build:  ## build docker image
	docker build -t $(DOCKER_IMG) .

.PHONY: check_env
check_env:
	@echo Checking environment ...
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry version

.PHONY: setup
setup:
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry update
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry lock

.PHONY: lint
lint:
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry run flake8 --verbose

.PHONY: test
test:
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry run pytest --verbose --color=yes pythonbot

.PHONY: coverage
coverage:
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry run pytest --cov-report term-missing:skip-covered --cov=pythonbot --verbose --color=yes

.PHONY: bump_py_version
bump_py_version:
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry version $(WHL_VERSION)

.PHONY: package
package: bump_py_version
	@echo Packaging application ...
	docker run --rm -v $(PWD):/workspace $(DOCKER_IMG) poetry build

.PHONY: clean
clean:
	@echo Cleaning environment ...
	# may not be a venv to remove, but just keep going in that case
	rm -rf *.egg-info build dist .coverage
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '.pytest_cache' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
