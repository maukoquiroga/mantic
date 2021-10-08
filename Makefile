.DEFAULT_GOAL := test

install:
	@pip install --upgrade pip poetry
	@poetry install

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

test: compile clean
	@poetry run pytest -qx

test-nox: test-nox-3.7.11 test-nox-3.8.12 test-nox-3.9.7 test-nox-3.10.0 ;

test-nox-%:
	@poetry run nox -p $*

bump:
	@git tag ${version}
	@git push --tags
