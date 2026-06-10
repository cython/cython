# cython: auto_cpdef=True
# mode: run
# tag: directive,auto_cpdef,dunders,cclass,richcmp,type_error
"""
Runtime behaviour when a cpdef richcmp dunder has a typed (extension-type)
second parameter and the comparison operand is an *incompatible* extension type.

The expression optimiser rewrites ``a == b`` on a final cclass into the method
call ``Vec2.__eq__(a, b)`` only when ``b`` is statically assignable to the typed
parameter.  An unrelated extension type is not assignable, so the rewrite is
skipped and the ordinary Python richcmp slot handles it at runtime.

The ``None`` literal against a 'not None' parameter is a *compile-time* error
and lives in tests/errors/cpdef_dunder_richcmp_type_errors.py.
"""
from __future__ import annotations
import cython
from cython import cclass, int as cint, final, bint


@final
@cclass
class Vec2:
    x: cint
    y: cint

    def __init__(self, x: cint, y: cint) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Vec2) -> bint:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: Vec2) -> bint:
        return self.x < other.x or (self.x == other.x and self.y < other.y)


@final
@cclass
class Point:
    x: cint
    y: cint

    def __init__(self, x: cint, y: cint) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Point) -> bint:
        return self.x == other.x and self.y == other.y


def eq_compatible():
    """
    >>> eq_compatible()
    True
    """
    a = Vec2(1, 2)
    b = Vec2(1, 2)
    return a == b


def lt_compatible():
    """
    >>> lt_compatible()
    True
    """
    a = Vec2(1, 2)
    b = Vec2(1, 3)
    return a < b


def eq_incompatible_extension_type():
    """
    Comparing against an unrelated extension type is not optimised to a direct
    C call (the operand is not statically assignable to the typed parameter), so
    the ordinary Python ``__eq__`` slot handles it.  In the compiled backends the
    slot rejects the foreign argument with a TypeError; in pure Python there is no
    argument coercion, so the comparison simply evaluates to a non-equal result.
    Either way the two objects are never reported as equal.

    >>> eq_incompatible_extension_type()
    True
    """
    a = Vec2(1, 2)
    p = Point(3, 4)
    try:
        return (a == p) is False
    except (TypeError, AttributeError):
        return True
