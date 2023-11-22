PROJECT_PATH = ./inclusive_dance_bot/
TEST_PATH = ./tests/

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

lint-ci: flake black bandit mypy  ##@Linting Run all linters in CI

flake: ##@Linting Run flake8
	.venv/bin/flake8 --max-line-length 88 --format=default $(PROJECT_PATH) 2>&1 | tee flake8.txt

black: ##@Linting Run black
	.venv/bin/black $(PROJECT_PATH) --check

bandit: ##@Linting Run bandit
	.venv/bin/bandit -r -ll -iii $(PROJECT_PATH) -f json -o ./bandit.json

mypy: ##@Linting Run mypy
	.venv/bin/mypy --config-file ./pyproject.toml $(PROJECT_PATH)

test: ##@Test Run tests with pytest
	pytest -vvx $(TEST_PATH)

test-ci: ##@Test Run tests with pytest and coverage in CI
	.venv/bin/pytest $(TEST_PATH) --junitxml=./junit.xml --cov=$(PROJECT_PATH) --cov-report=xml

develop: #
	python -m venv .venv
	.venv/bin/pip install -U pip poetry
	.venv/bin/poetry config virtualenvs.create false
	.venv/bin/poetry install

local: ##@Develop Run db and redis containers
	docker-compose -f docker-compose.dev.yaml up --force-recreate --renew-anon-volumes --build

local_down: ##@Develop Stop containers with delete volumes
	docker-compose -f docker-compose.dev.yaml down -v