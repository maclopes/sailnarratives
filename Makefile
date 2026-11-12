# Narrative engine for the Tagus sailing game
PYTHON ?= python3
VENV   ?= .venv
PY     := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip

.PHONY: setup setup-py setup-ts test test-py test-ts lint lint-py lint-ts validate clean

setup: setup-py setup-ts

setup-py:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

setup-ts:
	cd runtime && npm install

test: test-py test-ts

test-py:
	$(PY) -m pytest

test-ts:
	cd runtime && npm test

lint: lint-py lint-ts

lint-py:
	$(VENV)/bin/ruff check pipeline/src tests
	$(VENV)/bin/ruff format --check pipeline/src tests
	$(VENV)/bin/mypy

lint-ts:
	cd runtime && npm run lint
	runtime/node_modules/.bin/tsc -p domains/sailing/tsconfig.json

# Validate line files: make validate FILES="lines/draft/*.json"
FILES ?= domains/*/examples/*.json
validate:
	$(PY) -m tagus_narrative.validate $(FILES)

clean:
	rm -rf $(VENV) runtime/node_modules runtime/dist .pytest_cache .mypy_cache .ruff_cache
