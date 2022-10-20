.PHONY: install format lint test sec

install:
	@poetry install

format:
	black .
	isort .
	pyupgrade --py310-plus **/*.py

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
