# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Help view.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Sequence, Tuple

import deal
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import pysemver
import pysemver_hypothesis
from pysemver import utils

from .. import __version__
from ._base import columns, rows
from ._theme import Theme

pysemver_hypothesis.register(Layout(''))
pysemver_hypothesis.register(Panel(''))
pysemver_hypothesis.register(Table(''))

_headers = "Flags", "Description", "Default values"
"""Help command headers."""


@deal.pure
@utils.pipes
def _root(main: Panel) -> Layout:
    """Global help container.

    Args:
        main: Main container to wrap.

    Returns:
        Layout: To render.

    Examples:
        >>> content = _content(())
        >>> main = _main("command", content)
        >>> _root(main)
        Layout()

    .. versionadded:: 1.0.0

    """

    return main >> rows >> columns


@deal.pure
@utils.pipes
def _main(command: str, content: Table) -> Panel:
    """Main help container.

    Args:
        content: The inner container.

    Returns:
        The outer panel.

    Examples:
        >>> content = _content(())
        >>> main = _main("command", content)
        >>> main.title
        ...command...

    .. versionadded:: 1.0.0

    """

    return Panel(
        content,
        border_style = Theme.Console.BORDER,
        padding = 5,
        title = _usage(command),
        subtitle = __version__,
        )


@deal.pure
@utils.pipes
def _content(options: Sequence[Tuple[str, str, str]]) -> Table:
    """Inner usage instructions content.

    Args:
        options:
            A sequence of triples containing the flags, descriptions, and
            default values, for each option.

    Returns:
        The main content.

    Examples:
        >>> content = _content([("-f --flag", "How?", "Like that!")])
        >>> list(map(lambda option: option._cells, content.columns))
        [['-f --flag'], ['How?'], ['Like that!']]

        >>> content = _content([("", "", "")])
        >>> list(map(lambda option: option._cells, content.columns))
        [[''], [''], ['']]

    .. versionadded:: 1.0.0

    """

    table = Table(
        box = None,
        padding = (0, 5, 1, 10),
        row_styles = [Theme.Console.ROW],
        style = Theme.Console.HEADER,
        )

    (
        _headers
        << map(table.add_column)
        << tuple
        )

    (
        options
        << utils.dmap(table.add_row)
        << tuple
        )

    return table


@deal.pure
@utils.pipes
def _usage(command: str) -> Text:
    """Usage instructions.

    Examples:
        >>> _usage("command")
        <text 'Usage: pysemver command [--options] …' ...>

    .. versionadded:: 1.0.0

    """

    return (
        pysemver.__name__
        << str.format("Usage: {1} {0} [--options] …", command)
        >> Text
        << utils.partial(Text.stylize)
        >> utils.partial(Theme.Console.TITLE)
        >> utils.do
        )
