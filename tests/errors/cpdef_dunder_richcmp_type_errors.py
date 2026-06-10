# cython: auto_cpdef=True
# mode: error
# tag: directive,auto_cpdef,dunders,cclass,richcmp,type_error
"""
A cpdef richcmp dunder with a typed (non-None) extension-type second parameter
makes ``a == None`` / ``a < None`` a compile-time error.

The expression optimiser rewrites ``a == b`` on a final cclass into the method
call ``Vec2.__eq__(a, b)``.  Argument coercion then follows the normal rules for
an annotated extension-type parameter: ``None`` against a parameter that is
declared 'not None' (which is the default for an annotated extension type) is
rejected at compile time, exactly like any other typed call where a statically
known ``None`` literal is passed to a 'not None' parameter.
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


def eq_none():
    a = Vec2(1, 2)
    return a == None


def lt_none():
    a = Vec2(1, 2)
    return a < None


_ERRORS = """
39:16: Cannot pass None as argument 'other' which is declared 'not None'
44:15: Cannot pass None as argument 'other' which is declared 'not None'
"""
