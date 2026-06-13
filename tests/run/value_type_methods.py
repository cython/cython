# mode: run
# tag: dataclass, value_type, pure3.0

from __future__ import annotations

import cython
from cython import cclass, final, value_type
from dataclasses import dataclass


@value_type
@final
@cclass
@dataclass(frozen=True)
class Vec2:
    x: cython.double
    y: cython.double = 0.0

    def length2(self) -> cython.double:
        # Method returning a C scalar.
        return self.x * self.x + self.y * self.y

    def scaled(self, k: cython.double) -> Vec2:
        # Method returning the value type itself.
        return Vec2(self.x * k, self.y * k)

    @property
    def first(self) -> cython.double:
        return self.x

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)


@value_type
@final
@cclass
@dataclass(frozen=True)
class TupleHolder:
    # A ctuple field works (the ctuple struct is embedded by value).
    coords: tuple[cython.double, cython.double]
    flag: cython.bint = False

    def first_coord(self) -> cython.double:
        return self.coords[0]


@value_type
@final
@cclass
@dataclass(frozen=True)
class Divider:
    n: cython.double

    @cython.exceptval(check=True)
    def divide(self, d: cython.double) -> cython.double:
        if d == 0.0:
            raise ZeroDivisionError("division by zero")
        return self.n / d


# NOTE (v1 limitations, verified empirically):
#  * Nested value-type fields (a value_type field whose type is ANOTHER
#    value_type class) are NOT supported: the synthesized __hash__/__eq__ try
#    to hash/compare the embedded value struct as a Python object and the
#    compiler rejects it.  Use a ctuple field instead.
#  * Scalar reflected operators like `v * 2.0` (a value-type __mul__ with a
#    non-value-type operand) are not dispatched through the value dunder.
#    Use an explicit method (e.g. `v.scaled(2.0)`).
#  * `cpdef enum` fields work only in .pyx sources (pure-mode .py has no
#    cpdef-enum syntax); covered indirectly there.


@cython.ccall
def hot_make_and_add(a: cython.double, b: cython.double) -> Vec2:
    # A hot compiled path exercising stack construction + value-ABI __add__.
    return Vec2(a, b) + Vec2(1.0, 1.0)


def method_scalar_return():
    """
    >>> method_scalar_return()
    25.0
    """
    return Vec2(3.0, 4.0).length2()


def method_value_return():
    """
    >>> method_value_return()
    (6.0, 8.0)
    """
    v = Vec2(3.0, 4.0).scaled(2.0)
    return v.x, v.y


def property_access_on_value():
    """
    >>> property_access_on_value()
    3.0
    """
    # NOTE: a property access directly on a ctor-expression
    # (`Vec2(3.0, 4.0).first`) is not supported in v1; bind to a local first.
    v = Vec2(3.0, 4.0)
    return v.first


def property_access_on_boxed():
    """
    >>> property_access_on_boxed()
    3.0
    """
    o: object = Vec2(3.0, 4.0)
    return o.first


def binop_add():
    """
    >>> binop_add()
    (4.0, 5.0)
    """
    w = Vec2(3.0, 4.0) + Vec2(1.0, 1.0)
    return w.x, w.y


def binop_sub():
    """
    >>> binop_sub()
    (2.0, 3.0)
    """
    w = Vec2(3.0, 4.0) - Vec2(1.0, 1.0)
    return w.x, w.y


def unary_neg():
    """
    >>> unary_neg()
    (-3.0, -4.0)
    """
    w = -Vec2(3.0, 4.0)
    return w.x, w.y


def hot_path():
    """
    >>> hot_path()
    (4.0, 5.0)
    """
    v = hot_make_and_add(3.0, 4.0)
    return v.x, v.y


def method_on_boxed_instance():
    """
    Methods called on a boxed instance from Python still work (via the type's
    Python wrapper).

    >>> method_on_boxed_instance()
    (25.0, (6.0, 8.0))
    """
    o: object = Vec2(3.0, 4.0)
    scaled = o.scaled(2.0)
    return o.length2(), (scaled.x, scaled.y)


def ctuple_field():
    """
    >>> ctuple_field()
    (1.0, True, 1.0)
    """
    t = TupleHolder((1.0, 2.0), True)
    return t.coords[0], t.flag, t.first_coord()


def exceptval_method():
    """
    >>> exceptval_method()
    (5.0, True)
    """
    d = Divider(10.0)
    ok = d.divide(2.0)
    raised = False
    try:
        d.divide(0.0)
    except ZeroDivisionError:
        raised = True
    return ok, raised
