DATA_DIR=data/
BACKEND_DIR=api/
APP_DIR=app/

test-data:
	uv run --project data/ pytest data/test/
