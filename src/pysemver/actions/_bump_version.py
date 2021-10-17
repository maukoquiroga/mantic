# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Version bumber."""

from typing import Sequence, Tuple, Type

import re

import deal
import typic

from .. import infra
from ..domain import Version


@typic.klass(always = True, slots = True, strict = True)
class BumpVersion:
    """Determines the required version bump.

    Attributes:
        this: The actual version.
        that: The last tagged version.
        what: An ``event`` and the associated bump requirement.
        required: The required version bump.

    Examples:
        >>> bumper = BumpVersion()

        >>> bumper.required
        <Int.NONE: 0>

        >>> bumper.what(3)
        <Int.MAJOR: 3>

        >>> bumper(3)
        >>> bumper.required
        <Int.MAJOR: 3>

    .. versionadded:: 36.1.0

    """

    this: str
    that: str
    what: Type[Version.Int]
    required: Version.Int

    @deal.pure
    def __init__(self) -> None:
        self.this = infra.repo.versions.this()
        self.that = infra.repo.versions.last()
        self.what = Version.Int
        self.required = Version.Int.NONE

    @deal.pure
    # @typic.al(strict = True)
    def __call__(self, bump: int) -> None:
        """Bumps the required version."""

        index = max(self.required.value, Version.Int(bump).value)
        self.required = Version.Int(index)

    @deal.pure
    # @typic.al(strict = True)
    def is_acceptable(self) -> bool:
        """Determines if the current version is acceptable or not.

        Returns:
            True: When it is acceptable.
            False: Otherwise.

        Examples:
            >>> bumper = BumpVersion()
            >>> bumper.is_acceptable()
            True

            >>> bumper(3)
            >>> bumper.this = "1.2.3"
            >>> bumper.that = "1.2.3"
            >>> bumper.is_acceptable()
            False

            >>> bumper.this = "2.0.0"
            >>> bumper.is_acceptable()
            True

            >>> bumper.this = "2.0.0-rc.1+1234"
            >>> bumper.is_acceptable()
            True

            >>> bumper.that = "2.0.0-asdf+1234"
            >>> bumper.is_acceptable()
            True

        .. versionadded:: 36.1.0

        """

        actual_number: int
        actual_is_rel: bool
        before_number: int
        before_is_rel: bool

        # If there's no required bump, we just do not check.
        if self.required == Version.Int.NONE:
            return True

        # We get the actual number and whether it is a release or not.
        actual_number, actual_is_rel = self._extract(self.this)

        # We get the last tagged number and whether it is a release or not.
        before_number, before_is_rel = self._extract(self.that)

        # If both are releases, next version has to be major/minor/patch +1.
        if actual_is_rel and before_is_rel:
            before_number += 1

        # Otherwise we just do not check.
        # It is way too anecdotic for the complexity that the check requires.
        return actual_number >= before_number

    @deal.pure
    # @typic.al(strict = True)
    def _extract(self, version: str) -> Tuple[int, bool]:
        """Extract a major/minor/patch number from a version string."""

        is_release: bool
        release: str
        rest: Sequence[str]

        # We separate the non-release par, ex: ``-pre+1``.
        release, *rest = re.split("\\+|\\-", version)

        # We get the major/minor/patch number based on the required bump.
        number: str = release.split(".")[3 - self.required.value]

        # Finally we determine if this is a release or not.
        is_release = len(rest) == 0

        return int(number), is_release
