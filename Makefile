.PHONY: install install-dev doctor fixtures test test-unit test-integration manifest clean-work

install:
	python3 -m pip install -e .

install-dev:
	python3 -m pip install -e ".[dev]"

doctor:
	python3 -m clipkit --json doctor

fixtures:
	python3 scripts/generate_fixtures.py

test: fixtures
	python3 -m pytest

test-unit:
	python3 -m pytest -m "not integration"

test-integration: fixtures
	python3 -m pytest -m integration

manifest:
	python3 scripts/build_repository_manifest.py

clean-work:
	python3 scripts/clean_work.py --yes

