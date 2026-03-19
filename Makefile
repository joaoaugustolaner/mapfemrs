.PHONY: all test clean

test-data:
	uv run pytest -s -x --cov=src/data/spiders -vv
