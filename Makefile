.PHONY: install lint format format-check typecheck test coverage quality clean

install:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

typecheck:
	uv run mypy src/

test:
	uv run pytest

coverage:
	uv run pytest --cov=northstar --cov-report=term-missing

quality: lint format-check typecheck test

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
