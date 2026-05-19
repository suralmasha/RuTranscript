
package:
	poetry build

test:
	poetry run python -m unittest discover -s tests

ruff:
	poetry run ruff format
	poetry run ruff check --fix

ruff-check:
	poetry run ruff check

ruff-format-check:
	poetry run ruff format --check

ruff-fix:
	poetry run ruff check --fix
ruff-unsafe-fix:
	poetry run ruff check --fix --unsafe-fixes
ruff-format:
	poetry run ruff format

pre-commit:
	poetry run pre-commit install
