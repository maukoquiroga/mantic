from __future__ import annotations

import sys

import invoke
from invoke import Collection, Program
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pysemver import Bar, SupportsProgress
from pysemver import CheckDeprecated, CheckVersion

from ._types import HasExit

bar: SupportsProgress = Bar()


@invoke.task
def check_deprecated(_context):
    """Check if there are features to deprecate."""

    task: HasExit
    task = CheckDeprecated(bar)
    task()
    sys.exit(task.exit.value)


@invoke.task
def check_version(_context):
    """Check if the actual version is valid."""

    task: HasExit
    task = CheckVersion(bar)
    task()
    sys.exit(task.exit.value)


class CLI(Program):

    console = Console()
    tasks = Collection()

    def __init__(self) -> None:
        self.tasks.add_task(check_deprecated)
        self.tasks.add_task(check_version)
        super().__init__(namespace = self.tasks)

    def print_help(self) -> None:
        title = (f"Usage: {self.binary} <command> [--command-opts] …\n")
        content = self._build_content()
        self.console.print(Panel.fit(content, title = title))

    def task_list_opener(self, extra: str = "") -> str:
        return "Commands"

    def _build_content(self) -> Table:
        table = Table(box = None)
        table.add_column("Command")
        table.add_column("Description")

        for command, description in self._make_pairs(self.scoped_collection):
            table.add_row(command, description)

        return table


cli = CLI()
