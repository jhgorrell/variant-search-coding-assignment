
from __future__ import (
    absolute_import,
)

import sys
from typing import (
    Any,
)

#####


def safe_int(value, default=None):
    """Turn a value into an int; default if it cant be."""
    rv = default
    try:
        rv = int(value)
    except BaseException:
        pass
    return rv


def cast_rv(rv: Any) -> int:
    """
    Cast a python return value to a unix (single byte) return value.

    :param rv: int
    """
    if sys.stdout:
        sys.stdout.flush()
    if sys.stderr:
        sys.stderr.flush()
    if rv is True:
        return 0
    if rv is None or rv is False:
        return -1
    return rv
