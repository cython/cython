# cython: auto_cpdef=True
# mode: run
# tag: directive,auto_cpdef,dunders
from __future__ import annotations
import cython
from cython import cclass, int as cint, final, bint


@final
@cclass
class Vec2:
    x: cint
    y: cint

    def __init__(self, x: cint, y: cint):
        self.x = x
        self.y = y

    def coords(self) -> tuple[cint, cint]:
        return self.x, self.y

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def __eq__(self, other: Vec2) -> bint:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        # __repr__ is NOT in the whitelist — must stay as plain def
        return "Vec2(%d, %d)" % (self.x, self.y)


@cclass
class VecBase:
    x: cint
    y: cint

    def __init__(self, x: cint, y: cint):
        self.x = x
        self.y = y

    def coords(self) -> tuple:
        return (self.x, self.y)

    def __add__(self, other: VecBase) -> VecBase:
        return VecBase(self.x + other.x, self.y + other.y)


@final
@cclass
class VecSub(VecBase):
    def __add__(self, other: VecBase) -> VecBase:
        return VecSub(self.x + other.x + 10, self.y + other.y + 10)


def test_binop_promoted():
    """
    >>> test_binop_promoted()
    (3, 7)
    """
    a = Vec2(1, 3)
    b = Vec2(2, 4)
    c: Vec2 = a + b
    print(c.coords())


def test_binop_promoted_expr():
    """
    >>> test_binop_promoted_expr()
    (3, 7)
    """
    a = Vec2(1, 3) + Vec2(2, 4)
    print(a.coords())


def test_unop_promoted():
    """
    >>> test_unop_promoted()
    (-1, -2)
    """
    a = Vec2(1, 2)
    b: Vec2 = -a
    print(b.coords())


def test_sub_promoted():
    """
    >>> test_sub_promoted()
    (1, 2)
    """
    a = Vec2(3, 5)
    b = Vec2(2, 3)
    c: Vec2 = a - b
    print(c.coords())


def test_eq_promoted():
    """
    >>> test_eq_promoted()
    True
    False
    """
    a = Vec2(1, 2)
    b = Vec2(1, 2)
    c = Vec2(1, 3)
    print(a == b)
    print(a == c)


def test_repr_not_promoted():
    """
    Test that __repr__ is not in the whitelist and stays as plain def.
    >>> test_repr_not_promoted()
    Vec2(1, 2)
    """
    a = Vec2(1, 2)
    print(repr(a))



def test_inherited_dunder():
    """
    >>> test_inherited_dunder()
    (13, 17)
    """
    a = VecSub(1, 3)
    b = VecBase(2, 4)
    c: VecBase = a + b
    print(c.coords())
