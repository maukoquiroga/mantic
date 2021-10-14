# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import inspect

import pipeop
from invoke import Program
from rich.console import Console

from pysemver.infra import versions

from ._tasks import Tasks
from ._views import Help, Home

version = versions.this()


class Main(Program):

    tasks = Tasks()
    write = Console().print

    def __init__(self) -> None:
        super().__init__(namespace = self.tasks, version = version)

    @pipeop.pipes
    def print_help(self) -> None:
        (
            self.scoped_collection
            >> self._make_pairs
            >> Home.content
            >> Home.main
            >> Home.root
            >> self.write
            )

    @pipeop.pipes
    def print_task_help(self, command: str) -> None:
        context = self.parser.contexts >> dict.get(command)
        description = self.collection >> Tasks.__getitem__(command)
        documentation = inspect.getdoc(description)

        (
            context.help_tuples()
            << Help.content(documentation)
            << Help.main(command)
            >> Help.root
            >> self.write
            )

    def task_list_opener(self, __: str = "") -> str:
        return "Commands"


main = Main()