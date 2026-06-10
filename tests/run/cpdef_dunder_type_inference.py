# cython: auto_cpdef=True
# mode: run
# tag: directive,auto_cpdef,dunders,type_inference
"""
Type-inference tests for cpdef dunder expression optimisation.

These tests verify that when a binary/unary operator is applied to a final
extension type whose dunder is a cpdef method, the result type is inferred
from the dunder's C return type (not py_object_type), allowing the compiler
to eliminate Python-level boxing and to propagate the narrower type into
downstream expressions without extra casts.
"""
from __future__ import annotations
import cython
from cython import cclass, int as cint, double as cdouble, bint, final


@final
@cclass
class Vec2:
    x: cint
    y: cint

    def __init__(self, x: cint, y: cint) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def __mul__(self, scale: cint) -> Vec2:
        return Vec2(self.x * scale, self.y * scale)

    def __eq__(self, other: Vec2) -> bint:
        if not isinstance(other, Vec2):
            return False
        o = cython.cast(Vec2, other)
        return self.x == o.x and self.y == o.y

    def coords(self) -> tuple:
        return (self.x, self.y)

    def length_sq(self) -> cint:
        return self.x * self.x + self.y * self.y


@final
@cclass
class Scalar:
    """Extension type whose __add__ returns a built-in Python int (py_object),
    so no expression-level optimisation applies."""
    v: cint

    def __init__(self, v: cint) -> None:
        self.v = v

    def __add__(self, other) -> object:
        # Returns NotImplemented for non-Scalar — no typed return, not promoted.
        if not isinstance(other, Scalar):
            return NotImplemented
        return Scalar(self.v + cython.cast(Scalar, other).v)


# ---------------------------------------------------------------------------
# Inference: result of promoted binop is Vec2, not object
# ---------------------------------------------------------------------------

def test_add_result_type_is_vec2():
    """Verify add result can be assigned to a Vec2 variable and used directly.
    >>> test_add_result_type_is_vec2()
    (3, 7)
    """
    a = Vec2(1, 3)
    b = Vec2(2, 4)
    c: Vec2 = a + b          # type must be inferred as Vec2 for this to compile
    print(c.coords())


def test_sub_result_type_is_vec2():
    """
    >>> test_sub_result_type_is_vec2()
    (1, 2)
    """
    a = Vec2(3, 5)
    b = Vec2(2, 3)
    c: Vec2 = a - b
    print(c.coords())


def test_unop_result_type_is_vec2():
    """
    >>> test_unop_result_type_is_vec2()
    (-1, -2)
    """
    a = Vec2(1, 2)
    b: Vec2 = -a
    print(b.coords())


def test_mul_result_type_is_vec2():
    """Scalar multiplication: Vec2 * cint → Vec2.
    >>> test_mul_result_type_is_vec2()
    (4, 10)
    """
    a = Vec2(2, 5)
    b: Vec2 = a * 2
    print(b.coords())


# ---------------------------------------------------------------------------
# Inference: result of eq is bint, allows direct use in bool context
# ---------------------------------------------------------------------------

def test_eq_result_is_bint():
    """__eq__ with bint return: result usable as C int, not object.
    >>> test_eq_result_is_bint()
    True
    False
    """
    a = Vec2(1, 2)
    b = Vec2(1, 2)
    c = Vec2(3, 4)
    # Using the result in an if statement exercises bint inference
    if a == b:
        print(True)
    else:
        print(False)
    if a == c:
        print(True)
    else:
        print(False)


# ---------------------------------------------------------------------------
# Inference: chained operations — result of inner op feeds outer op
# ---------------------------------------------------------------------------

def test_chained_add():
    """(a + b) + c — the inner add result must be typed Vec2 for the outer
    add to also be optimised.
    >>> test_chained_add()
    (6, 12)
    """
    a = Vec2(1, 2)
    b = Vec2(2, 4)
    c = Vec2(3, 6)
    d: Vec2 = a + b + c
    print(d.coords())


def test_chained_unop_and_binop():
    """(-a) + b: unop result is Vec2, so the outer binop is also optimised.
    >>> test_chained_unop_and_binop()
    (1, 2)
    """
    a = Vec2(-1, -2)
    b = Vec2(0, 0)
    # (-a) has type Vec2; Vec2.__add__ is cpdef so the whole expr is optimised
    c: Vec2 = (-a) + b
    print(c.coords())


def test_method_call_on_optimised_result():
    """Use an optimised binop result immediately as the receiver of a method call.
    This verifies the inferred type flows into downstream attribute accesses.
    >>> test_method_call_on_optimised_result()
    25
    """
    a = Vec2(0, 0)
    b = Vec2(3, 4)
    # length_sq of (0+3, 0+4) = 3^2 + 4^2 = 25
    lsq: cint = (a + b).length_sq()
    print(lsq)


# ---------------------------------------------------------------------------
# Inference: no optimisation for non-final or non-cpdef types
# ---------------------------------------------------------------------------

def test_non_typed_return_not_optimised():
    """Scalar.__add__ returns object (and can return NotImplemented), so
    the expression must still work at the Python level.
    >>> test_non_typed_return_not_optimised()
    3
    """
    a = Scalar(1)
    b = Scalar(2)
    c = a + b
    # c is Scalar — access .v via Python attribute
    print(cython.cast(Scalar, c).v)


# ---------------------------------------------------------------------------
# Inference: mixed-type operands (extension type op different type)
# ---------------------------------------------------------------------------

def test_mul_with_literal():
    """Vec2 * literal int — operand2 is IntNode, type must be assignable to cint.
    >>> test_mul_with_literal()
    (6, 9)
    """
    a = Vec2(3, 4)
    # scale operand is a Python int literal; Cython coerces to cint
    b: Vec2 = a * cython.cast(cint, 3) - Vec2(3, 3)
    # (9,12) - (3,3) = (6,9)
    print(b.coords())
