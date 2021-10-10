.DEFAULT_GOAL := all

all: format lint type test ;

install:
	@pip install --upgrade pip wheel setuptools
	@pip install --upgrade poetry

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

format: $(shell git ls-files "*.py")
	@poetry run autopep8 $?
	@poetry run pyupgrade $? --py36-plus --keep-runtime-typing

lint: compile clean
	@poetry run flake8 docs/conf.py src tests noxfile.py

type: compile clean
	@poetry run mypy docs/conf.py src noxfile.py
	@poetry run pytype docs/conf.py src noxfile.py

test: compile clean
	@poetry run pytest --cov

release:
	@poetry run nox
	@poetry run pip uninstall pysemver -y -q
	@poetry install -q
	@poetry run pysemver check-version \
		&& exit_code=$${?} \
		|| exit_code=$${?} \
		&& version=( "" "patch" "minor" "major" ) \
		&& poetry version $${version[$${exit_code}]} -q \
		&& poetry install -q \
		&& git add -A \
		&& poetry version --short | xargs -I \{\} git commit -m "Bump version to {}" \
		&& poetry version --short | xargs -I \{\} git tag \{\} \
		&& git push --tags
