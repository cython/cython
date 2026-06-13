# mode: run
# tag: dataclass, value_type, pure3.0

from __future__ import annotations

import cython
from cython import cclass, final, value_type
from dataclasses import dataclass
import dataclasses


@value_type
@final
@cclass
@dataclass(frozen=True)
class Vec2:
    x: cython.double
    y: cython.double = 0.0


@cython.ccall
def box(v: Vec2) -> object:
    # Returning a value struct into an object context boxes it (new object).
    return v


@cython.ccall
def unbox(o: object) -> Vec2:
    # Coercing an object into the value type does an exact-type check + copy.
    w: Vec2 = o
    return w


@cython.ccall
def typeof_in_compiled() -> str:
    v = Vec2(1.0, 2.0)
    return cython.typeof(v)


def make_positional():
    """
    >>> make_positional()
    (3.0, 4.0)
    """
    v = Vec2(3.0, 4.0)
    return v.x, v.y


def make_keyword():
    """
    >>> make_keyword()
    (1.0, 2.0)
    """
    v = Vec2(x=1.0, y=2.0)
    return v.x, v.y


def make_default():
    """
    >>> make_default()
    (5.0, 0.0)
    """
    v = Vec2(5.0)
    return v.x, v.y


def typeof_value():
    """
    cython.typeof of a value struct reports the class name.

    >>> typeof_value()
    'Vec2'
    """
    return typeof_in_compiled()


def boxing_identity():
    """
    Each box produces a *distinct* object (identity is not preserved, like
    ctuple->tuple), but the boxed objects compare equal by value.  (In pure
    Python the class is a normal frozen dataclass so identity IS preserved;
    the value-semantics claim is compiled-only.)

    >>> boxing_identity()
    (True, True)
    """
    v = Vec2(3.0, 4.0)
    o1 = box(v)
    o2 = box(v)
    distinct = (o1 is not o2) if cython.compiled else True
    return distinct, (o1 == o2)


def box_into_object_and_list():
    """
    >>> box_into_object_and_list()
    (3.0, 4.0)
    """
    v = Vec2(3.0, 4.0)
    o: object = v
    lst = [v]
    return o.x, lst[0].y


def unbox_roundtrip():
    """
    >>> unbox_roundtrip()
    (7.0, 8.0)
    """
    o = box(Vec2(7.0, 8.0))
    v = unbox(o)
    return v.x, v.y


def unbox_rejects_none():
    """
    Unboxing None must raise TypeError (exact-type unbox).

    >>> unbox_rejects_none()
    True
    """
    if not cython.compiled:
        return True  # pure Python: the annotation is a no-op, no exact-type unbox
    try:
        unbox(None)
        return False
    except TypeError:
        return True


def unbox_rejects_dict():
    """
    A dict with matching keys is rejected -- the value struct did NOT inherit
    the cython.struct mapping converter.

    >>> unbox_rejects_dict()
    True
    """
    if not cython.compiled:
        return True  # pure Python: the annotation is a no-op, no exact-type unbox
    try:
        unbox({'x': 1.0, 'y': 2.0})
        return False
    except TypeError:
        return True


def dataclass_fields_work():
    """
    >>> dataclass_fields_work()
    ['x', 'y']
    """
    return [f.name for f in dataclasses.fields(Vec2)]


def isinstance_of_boxed():
    """
    >>> isinstance_of_boxed()
    True
    """
    o = box(Vec2(1.0, 2.0))
    return isinstance(o, Vec2)


def repr_of_boxed():
    """
    >>> repr_of_boxed()
    'Vec2(x=3.0, y=4.0)'
    """
    return repr(box(Vec2(3.0, 4.0)))


def value_copy_semantics():
    """
    Assigning a value struct copies it; the two boxes are independent objects
    holding equal values (fields are frozen, so we demonstrate copy via distinct
    boxed results that nonetheless compare equal).

    >>> value_copy_semantics()
    (True, True)
    """
    a = Vec2(1.0, 2.0)
    b = a  # value copy
    distinct = (box(a) is not box(b)) if cython.compiled else True
    return distinct, (box(a) == box(b))
