# cython: auto_cpdef=True
# mode: run
# tag: directive,auto_cpdef,dunders,dataclass
from __future__ import annotations
import cython
from cython import cclass, int as cint, final
import cython.dataclasses as dataclasses


@final
@cclass
@dataclasses.dataclass(frozen=True, order=True)
class Point:
    x: cint = 0
    y: cint = 0


def test_eq_and_order():
    """
    >>> test_eq_and_order()
    True
    False
    True
    False
    True
    """
    a = Point(1, 2)
    b = Point(1, 2)
    c = Point(2, 3)
    print(a == b)
    print(a == c)
    print(a < c)
    print(c < a)
    print(a != c)


def test_eq_none():
    """
    >>> test_eq_none()
    False
    """
    a = Point(1, 2)
    print(a == None)


def test_hash():
    """
    >>> test_hash()
    True
    """
    a = Point(1, 2)
    b = Point(1, 2)
    print(hash(a) == hash(b))
