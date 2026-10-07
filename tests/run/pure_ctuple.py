# cython: language_level=3
# mode: run
# tag: pure3.7, pep484, warnings

# for the benefit of the pure tests, don't require annotations
# to be evaluated
from __future__ import annotations

import typing
from typing import Tuple
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


# because tuple is specifically special cased to go to ctuple where possible
def test_tuple(a: typing.Tuple[cython.int, cython.float], b: typing.Tuple[cython.int, ...],
               c: Tuple[cython.int, object]  # cannot be a ctuple
               ):
    """
    >>> test_tuple((1, 1.0), (1, 1.0), (1, 1.0))
    int
    int object
    double
    double
    (int, float)
    tuple[int object,double] object
    tuple[int,...] object
    tuple[int,Python object] object
    tuple object
    """
    x: typing.Tuple[int, float] = (a[0], a[1])  # note: Python int/float, not cython.int/float
    y: Tuple[cython.int, ...] = (1,2.)
    plain_tuple: Tuple = ()
    z = a[0]  # should infer to C int
    p = x[1]  # should infer to Python float -> C double

    print(cython.typeof(z))
    print(cython.typeof(x[0]) + (" object" if not cython.compiled else ""))
    print(cython.typeof(p) if cython.compiled else 'double')
    print(cython.typeof(x[1]) if cython.compiled else 'double')
    print(cython.typeof(a) if cython.compiled or cython.typeof(a) != 'tuple' else "(int, float)")
    print(cython.typeof(x) + ("[int object,double] object" if not cython.compiled else ""))
    print(cython.typeof(y) + ("[int,...] object" if not cython.compiled else ""))
    print(cython.typeof(c) + ("[int,Python object] object" if not cython.compiled else ""))
    print(cython.typeof(plain_tuple) + (" object" if not cython.compiled else ""))

# because tuple is specifically special cased to go to ctuple where possible
def test_tuple_without_typing(a: tuple[cython.int, cython.float], b: tuple[cython.int, ...],
               c: tuple[cython.int, object]  # cannot be a ctuple
               ):
    """
    >>> test_tuple_without_typing((1, 1.0), (1, 1.0), (1, 1.0))
    int
    int
    double
    double
    (int, float)
    tuple[int object,double] object
    tuple[int,...] object
    tuple[int,Python object] object
    tuple object
    """
    x: tuple[int, float] = (a[0], a[1])  # note: Python int/float, not cython.int/float
    y: tuple[cython.int, ...] = (1,2.)
    plain_tuple: tuple = ()
    z = a[0]  # should infer to C int
    p = x[1]  # should infer to Python float -> C double

    print(cython.typeof(z))
    print("int" if cython.compiled and cython.typeof(x[0]) == "int object" else cython.typeof(x[0]))
    print(cython.typeof(p) if cython.compiled or cython.typeof(p) != 'float' else "double")
    print(cython.typeof(x[1]) if cython.compiled or cython.typeof(p) != 'float' else "double")
    print(cython.typeof(a) if cython.compiled or cython.typeof(a) != 'tuple' else "(int, float)")
    print(cython.typeof(x) + ("[int object,double] object" if not cython.compiled else ""))
    print(cython.typeof(y) + ("[int,...] object" if not cython.compiled else ""))
    print(cython.typeof(c) + ("[int,Python object] object" if not cython.compiled else ""))
    print(cython.typeof(plain_tuple) + (" object" if not cython.compiled else ""))

_WARNINGS = """
"""
