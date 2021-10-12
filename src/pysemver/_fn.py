# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Somme handy functions to pipe data.

These are rather convenient for building the interface, and traversing the
AST and so on…

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import functools
import itertools
from typing import Any, Callable, Iterator, Sequence, Tuple, TypeVar

import deal

T = TypeVar("T", bound = Any)

partial = functools.partial
"""Just a shortcut for `.functools.partial`."""


@deal.pure
def _(x: T) -> Callable[..., T]:
    """Identity useful for noop.

    Examples:
        >>> _(1)()
        1

    .. versionadded:: 1.0.0

    """

    return lambda: x


@deal.pure
def do(func: Callable[[T], Any]) -> T:
    """Do something on something, thent return something.

    Args:
        func: Something.

    Returns:
        Any: The original thing.

    Examples:
        >>> x = "hey!"
        >>> func = partial(str.upper, x)
        >>> func()
        >>> do(func)
        'hey!'

    .. versionadded:: 1.0.0

    """

    self, *args = func.args

    func.func(self, *args, **func.keywords)

    return self


@deal.pure
def dfc(seqs: Sequence[Sequence[T]]) -> Iterator[Tuple[T, ...]]:
    """Like the original cons but for cons of cons.

    Args:
        seqs: Any sequences of sequences.

    Examples:
        >>> list(dfc[(1, [2, 3]), (4, [5, 6])]))
        [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

    .. versionadded:: 1.0.0

    """

    return (tuple(itertools.chain([el], seq)) for el, seq in seqs)


@deal.pure
def dfp(func: Callable[[T], T], seqs: Sequence[T]) -> Iterator[T]:
    """Applies a function to a sequence of sequences.

    Args:
        func: Any callable.
        seqs: Any sequence of sequences.

    Examples:
        >>> list(dfp(float.__add__, [(.1, .2), (.3, .4)]))
        [0.3..., 0.7]

    .. versionadded:: 1.0.0

    """

    return (func(*seq) for seq in seqs)


@deal.pure
def first(seq: Sequence[T]) -> T:
    """Returns the first element of a sequence.

    Args:
        seq: Any sequence.

    Examples:
        >>> first([1, 2, 3])
        1

    .. versionadded:: 1.0.0

    """

    return next(iter(seq))


@deal.pure
def compact(seq: Sequence[Any]) -> Iterator[Any]:
    """ Filters falsy values.

    Args:
        seq: Any sequence.

    Examples:
        >>> list(compact(["1", 0, "a", None, {}]))
        ['1', 'a']

    .. versionadded:: 1.0.0

    """

    return filter(bool, seq)


@deal.pure
def flatten(seqs: Sequence[Sequence[Any]]) -> Iterator[Any]:
    """Flattens a sequences of sequences.

    Args:
        seqs: Any sequence of sequences.

    Examples:
        >>> list(flatten([(1, 2), (3, 4)]))
        [1, 2, 3, 4]

        >>> list(flatten(["ab", "cd"]))
        ['a', 'b', 'c', 'd']

    .. versionadded:: 1.0.0

    """

    return itertools.chain.from_iterable(seqs)
