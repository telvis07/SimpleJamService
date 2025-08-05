.PHONY: env clean fmt lint test

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

test:
	uv run coverage run -m pytest tests/
	uv run coverage report --show-missing
