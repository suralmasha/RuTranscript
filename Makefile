
package:
	poetry build

test:
	poetry run python -m unittest discover -s tests

ruff:
	poetry run ruff format
	poetry run ruff check --fix
ruff-unsafe-fix:
	poetry run ruff check --fix --unsafe-fixes

pre-commit:
	poetry run pre-commit install
