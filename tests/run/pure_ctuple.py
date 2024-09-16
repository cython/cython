# cython: language_level=3
# mode: run
# tag: pure3.7, pep484, warnings

import typing
import cython


def test_optional_ctuple(x: typing.Optional[tuple[float]]):
    """
    Should not be a C-tuple (because these can't be optional)
    >>> test_optional_ctuple((1.0,))
    tuple object
    """
    print(cython.typeof(x) + (" object" if not cython.compiled else ""))


def test_union_ctuple(x: typing.Union[tuple[float], None]):
    """
    Should not be a C-tuple (because these can't be optional)
    >>> test_union_ctuple((1.0,))
    tuple object
    """
    print(cython.typeof(x) + (" object" if not cython.compiled else ""))


def test_bitwise_or_ctuple(x: tuple[float] | None, y: None | tuple[float]):
    """
    Should not be a C-tuple (because these can't be optional)
    >>> test_bitwise_or_ctuple((1.0,), (2.0,))
    tuple object
    tuple object
    """
    print(cython.typeof(x) + (" object" if not cython.compiled else ""))
    print(cython.typeof(y) + (" object" if not cython.compiled else ""))

_WARNINGS = """
"""
