PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

PACKAGE ?= src

.venv: pyproject.toml poetry.lock
	@poetry install

install: pyproject.toml poetry.lock ## Install the project
	@poetry install

lint: ## Lint the source code
	@poetry run isort $(PACKAGE)
	@poetry run black $(PACKAGE)
	@poetry run flake8 $(PACKAGE)
	@poetry run mypy --pretty $(PACKAGE)
