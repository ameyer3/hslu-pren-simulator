.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install:          ## Install the project in dev mode.
	@poetry install

.PHONY: fmt
fmt:              ## Format code using black & isort.
	poetry run isort .
	poetry run black -l 120 .

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	poetry run flake8 --max-line-length 120 .
	poetry run black -l 120 --check .
	poetry run mypy --ignore-missing-imports .

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	poetry run pytest -v --cov-config .coveragerc --cov=simulator -l --tb=short --maxfail=1 tests/
	poetry run coverage xml
	poetry run coverage html

.PHONY: run
run:              ## Run tests and generate coverage report.
	@poetry run python -m simulator

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build