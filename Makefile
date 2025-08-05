.PHONY: env clean fmt lint test tests

clean:
	rm -rf .venv
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf coverage.xml


env:
	uv sync

fmt:
	uv run ruff format simplejam/
	uv run ruff check simplejam/ --fix

lint:
	uv run ruff check simplejam/
	uv run mypy simplejam/

test tests:
	uv run coverage run --source=simplejam -m pytest tests/
	uv run coverage report --show-missing --fail-under=0
