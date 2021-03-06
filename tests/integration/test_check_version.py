# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

import sys

import pytest

from mantic import utils
from mantic.actions import CheckVersion
from mantic.domain import Exit
from mantic.infra import logs


@pytest.fixture
def checker():
    """A version checker."""

    checker = CheckVersion(logs, ignore = ("README.md",))
    checker.parser = type(checker.parser)(this = "0.2.0", that = "0.2.0")
    checker.bump_version.this = "0.2.0"
    checker.bump_version.that = "0.2.0"
    return checker


@pytest.fixture
def info(mocker, checker):
    return mocker.spy(logs, "info")


@pytest.fixture
def warn(mocker, checker):
    return mocker.spy(logs, "warn")


@pytest.fixture
def fail(mocker, checker):
    return mocker.spy(logs, "fail")


@pytest.fixture
def okay(mocker, checker):
    return mocker.spy(logs, "okay")


@pytest.fixture
def calls(warn):
    def _calls():
        calls = warn.call_args_list
        calls = utils.flatten(calls)
        calls = map(utils.first, calls)
        calls = utils.compact(calls)
        return tuple(calls)

    return _calls


def test_check_version(info, okay, checker):
    """Prints status updates to the user."""

    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_any_call(f"Parsing files from {checker.parser.this}…\n")
    info.assert_any_call(f"Parsing files from {checker.parser.that}…\n")
    info.assert_any_call("Checking for functional changes…\n")
    info.assert_any_call("Checking for + functions…\n")
    info.assert_any_call("Checking for - functions…\n")
    info.assert_any_call("Version bump required: NONE!\n")
    okay.assert_called_once_with(f"Current version: {checker.parser.this}")
    assert exit.value.code == Exit.OK


def test_files_when_no_diff(info, warn, fail, okay, checker):
    """Passes when there are no file diffs."""

    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: NONE!\n")
    warn.assert_not_called()
    fail.assert_not_called()
    okay.assert_called()
    assert exit.value.code == Exit.OK


def test_files_when_diff_is_not_functional(info, warn, fail, okay, checker):
    """Does not require a version bump files are not functional."""

    checker.parser.diff = ("README.md",)
    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: NONE!\n")
    warn.assert_not_called()
    fail.assert_not_called()
    okay.assert_called()
    assert exit.value.code == Exit.OK


def test_files_when_diff_is_functional(info, warn, fail, checker):
    """Requires a patch bump when there are file diffs."""

    checker.parser.diff = ("file.py",)
    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: PATCH!\n")
    warn.assert_called_once_with("~ file.py\n")
    fail.assert_called()
    assert exit.value.code != Exit.OK


def test_files_when_diff_only_parse_changed(info, warn, fail, checker):
    """Only go inspect changed files."""

    checker.parser = type(checker.parser)(this = "0.2.5", that = "0.2.6")
    checker()
    warn.assert_called_with("+ pysemver._func_checker.function => MINOR\n")
    assert warn.call_count == 2

    checker.parser.diff = ()
    checker.logs.called = ()
    checker()
    assert warn.call_count == 2

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: MINOR!\n")
    fail.assert_called()
    assert exit.value.code != Exit.OK


def test_funcs_when_no_diff(info, warn, fail, okay, checker):
    """Does not warn if there are no diffs."""

    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: NONE!\n")
    warn.assert_not_called()
    fail.assert_not_called()
    okay.assert_called()
    assert exit.value.code == Exit.OK


def test_funcs_when_added(info, warn, fail, calls, checker):
    """Requires a minor bump when a function is added."""

    checker.parser = type(checker.parser)(this = "0.2.5", that = "0.2.4")
    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: MINOR!\n")

    added = list(map(lambda c: "+" in c, calls()))
    assert len(list(utils.compact(added))) == 1

    removed = list(map(lambda c: "-" in c, calls()))
    assert len(list(utils.compact(removed))) == 0

    fail.assert_called()

    assert exit.value.code != Exit.OK


def test_funcs_when_removed(info, warn, fail, calls, checker):
    """Requires a major bump when a function is removed."""

    checker.parser = type(checker.parser)(this = "0.2.6", that = "0.2.5")
    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: MAJOR!\n")

    added = list(map(lambda c: "+" in c, calls()))
    assert len(list(utils.compact(added))) == 0

    removed = list(map(lambda c: "-" in c, calls()))
    assert len(list(utils.compact(removed))) == 1

    fail.assert_called()

    assert exit.value.code != Exit.OK


def test_funcs_when_duplicates(info, warn, fail, checker):
    """Gives a unique name to all signatures in the same module."""

    checker.parser = type(checker.parser)(this = "0.2.8", that = "0.2.7")
    checker()

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    info.assert_called_with("Version bump required: MAJOR!\n")
    warn.assert_any_call("- pysemver._func_checker.score(bis) => MAJOR\n")
    warn.assert_any_call("- pysemver._func_checker.score(ter) => MAJOR\n")
    warn.assert_any_call("- pysemver._func_checker.score(quater) => MAJOR\n")
    warn.assert_any_call(
        "- pysemver._func_checker.score(quinquies) => MAJOR\n",
        )
    warn.assert_any_call("- pysemver._func_checker.score(sexies) => MAJOR\n")
    fail.assert_called()
    assert exit.value.code != Exit.OK
