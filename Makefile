# svg.shapes Makefile
root_dir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
bin_dir := $(root_dir)/.venv/bin/
python_exe := $(bin_dir)python3

.PHONY: help test test-coverage lint format type-check clean build install dev-install docs

help:
	@echo "Available targets:"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  lint          - Run linting checks"
	@echo "  format        - Format code with black"
	@echo "  type-check    - Run mypy type checking"
	@echo "  clean         - Clean build artifacts"
	@echo "  build         - Build distribution packages"
	@echo "  install       - Install package in development mode"
	@echo "  dev-install   - Install with development dependencies"

test:
	$(python_exe) -m pytest

test-coverage:
	$(python_exe) -m pytest --cov=svg.shapes --cov-report=html --cov-report=term-missing

lint:
	$(python) -m flake8 src/ tests/
	$(python) -m pyroma .
	$(python) -m check-manifest

format:
	$(python) -m black src/ tests/

type-check:
	$(python) -m mypy src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(python) -m build

devenv:
	uv venv
	uv pip install -e .[dev]

# Run all quality checks
check-all: lint type-check test-coverage

# Development workflow
dev: devenv format type-check test
