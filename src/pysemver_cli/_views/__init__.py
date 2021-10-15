# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Views, or interface, of pysemver.

Loosely based on the MVC thing, the idea is to have a clear separation of
concerns between the presentation layer and the rest of the package. Views
are mostly repetitive, but it is yet too soon to refactor them.

.. versionadded:: 1.0.0

"""

from . import _help_view as help_view  # noqa: F401
from . import _home_view as home_view  # noqa: F401
from ._to_options import to_options  # noqa: F401
