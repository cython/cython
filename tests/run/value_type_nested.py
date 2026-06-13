# mode: run
# tag: dataclass, value_type, pure3.0

from __future__ import annotations, print_function

import cython
from cython import cclass, final, value_type
from dataclasses import dataclass


@value_type
@final
@cclass
@dataclass(frozen=True)
class Inner:
    a: cython.double


@value_type
@final
@cclass
@dataclass(frozen=True)
class Outer:
    p: Inner
    q: cython.double


@cython.cfunc
def make_outer(a: cython.double, q: cython.double) -> Outer:
    """Construct via a cfunc — exercises the value ABI."""
    return Outer(Inner(a), q)


@cython.cfunc
def get_inner(o: Outer) -> Inner:
    """Pass Outer by value, return Inner by value."""
    return o.p


def test_construction():
    """
    >>> test_construction()
    1.0
    2.0
    """
    o = Outer(Inner(1.0), 2.0)
    print(o.p.a)
    print(o.q)


def test_eq_same():
    """
    >>> test_eq_same()
    True
    """
    o1: object = Outer(Inner(1.0), 2.0)
    o2: object = Outer(Inner(1.0), 2.0)
    print(o1 == o2)


def test_eq_diff_nested():
    """
    >>> test_eq_diff_nested()
    False
    """
    o1: object = Outer(Inner(1.0), 2.0)
    o2: object = Outer(Inner(9.0), 2.0)
    print(o1 == o2)


def test_ne():
    """
    >>> test_ne()
    True
    """
    o1: object = Outer(Inner(1.0), 2.0)
    o3: object = Outer(Inner(9.0), 2.0)
    print(o1 != o3)


def test_hash_equal():
    """
    >>> test_hash_equal()
    True
    """
    o1: object = Outer(Inner(1.0), 2.0)
    o2: object = Outer(Inner(1.0), 2.0)
    print(hash(o1) == hash(o2))


def test_hash_diff():
    """
    >>> test_hash_diff()
    True
    """
    o1: object = Outer(Inner(1.0), 2.0)
    o3: object = Outer(Inner(9.0), 2.0)
    print(hash(o1) != hash(o3))


def test_repr():
    """
    >>> test_repr()
    Outer(p=Inner(a=1.0), q=2.0)
    """
    o: object = Outer(Inner(1.0), 2.0)
    print(repr(o))


def test_cfunc_passbyvalue():
    """
    >>> test_cfunc_passbyvalue()
    1.5
    3.0
    """
    o = make_outer(1.5, 3.0)
    inner = get_inner(o)
    print(inner.a)
    print(o.q)


def test_in_dict_as_key():
    """
    >>> test_in_dict_as_key()
    found
    """
    o1: object = Outer(Inner(1.0), 2.0)
    o2: object = Outer(Inner(1.0), 2.0)
    d = {o1: "found"}
    print(d[o2])
