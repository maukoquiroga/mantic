.DEFAULT_GOAL := test

install:
	@pip install --upgrade pip wheel setuptools
	@pip install --upgrade poetry

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

test: compile clean
	@poetry run pytest -qx

release:
	@poetry run nox -s test
	@poetry run python -m pysemver CheckVersion \
		&& exit_code=$$? \
		|| exit_code=$$? \
		&& version=( "" "patch" "minor" "major" ) \
		&& poetry version $${version[$${exit_code}]} -q
	@poetry install -q
	@git add -A
	@git commit -m "Bump version to $(shell poetry version --short)"
	@git tag $(shell poetry version --short)
	@git push --tags
