all: install clean test lint

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

flake8:
	flake8 src/

format:
	black src
	isort src

install:
	pip install -e .[test]

lint:
	black --check --diff src
	isort --check-only --diff src
	flake8 src

test:
	py.test
