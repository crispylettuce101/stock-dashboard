.PHONY: install test run clean lint format help

PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run application"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) tests/ -v

coverage:
	$(PYTEST) tests/ --cov=src --cov-report=html --cov-report=term

run:
	$(PYTHON) -m src.main

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage

lint:
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=120

format:
	$(PYTHON) -m black src/ tests/ --line-length=120

init:
	mkdir -p data docs/images config .github/workflows
	touch data/.gitkeep
	cp .env.example .env 2>/dev/null || echo ".env exists"
