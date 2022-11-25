.PHONY: install format lint test sec

install:
	@poetry install

format:
	black .
	isort .

lint:
	@black . --check --diff --color .
	@flake8 .
	@isort --diff -c .
	@mypy .

pre-commit:
	poetry run pre-commit run

test:
	@pytest -v

sec:
	@pip-audit
