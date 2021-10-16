# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Main cli initialiser."""

from __future__ import annotations

import inspect

import typic
from invoke import Program
from invoke.parser.context import ParserContext

import pysemver_cli
from pysemver import utils

from ._tasks import Tasks
from ._views import help_view, home_view, to_options

_tasks: Tasks = Tasks()
#: The list of tasks.

_header: str = "Commands"
#: The home screen header opener.


@typic.klass(always = True, strict = True)
class Main(Program):
    """Interfaces with :mod:`.invoke`."""

    def __init__(self) -> None:
        super().__init__(
            namespace = _tasks,
            version = pysemver_cli.__version__,
            )

    @utils.pipes
    def print_help(self) -> None:
        """Intercepts :mod:`.invoke` to print the home screen."""

        return (
            _tasks
            >> self._make_pairs
            >> home_view.render
            )

    @utils.pipes
    def print_task_help(self, command: str) -> None:
        """Intercepts :mod:`.invoke` to print the help screen."""

        return (
            self.parser.contexts
            >> dict.get(command)
            >> ParserContext.help_tuples
            >> to_options
            << help_view.render(
                command,
                _tasks >> Tasks.__getitem__(command) >> inspect.getdoc,
                )
            )

    def task_list_opener(self, _command: str = "") -> str:
        """Intercepts :mod:`.invoke` to set the main header name."""

        return _header


main = Main()
