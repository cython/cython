# cython: auto_cpdef=True
# mode:run
# tag: directive,auto_cpdef

from cython import cclass, int, final, public


@cclass
class Base:
    """Simplest base case"""

    def mtd(self) -> int:
        # This function is automatically promoted to cpdef
        return 3


# Auto cpdef causes the fn() function becomes public, thus Vector needs to be public too.
@public
@cclass
class Vector:
    a: int
    b: int

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.a + other.a, self.b + other.b)

    def length_sq(self) -> int:
        # This function is automatically promoted to cpdef
        return self.a*self.a + self.b*self.b

    def __eq__(self, other) -> bool:
        return self.a == other.a and self.b == other.b

    def __repr__(self) -> str:
        return f"Vector({self.a}, {self.b})"


def fn() -> Vector:
    return Vector(2, 3)


def test_vector(v):
    """
    Just test a simple class with auto_cpdef enabled.

    >>> Base().mtd()
    3
    >>> test_vector(Vector(2, 3) + Vector(4, 5))
    Vector(6, 8)
    >>> test_vector(fn().length_sq())
    13
    """
    return v


@public
@final
@cclass
class VectorFinal(Vector):

    def length_sq(self) -> int:
        # This function is automatically promoted to cpdef
        return 23

    def origin_length_sq(self) -> int:
        # This function is automatically promoted to cpdef
        # accessing base class through super() is optimized too
        return super().length_sq()


def fn2() -> VectorFinal:
    return VectorFinal(2, 3)


def test_vector_final(v):
    """
    Just test a simple final class with auto_cpdef enabled.

    >>> test_vector(VectorFinal(2, 3) + VectorFinal(4, 5))
    Vector(6, 8)
    >>> test_vector(VectorFinal(2, 3).length_sq())
    23
    >>> test_vector(fn2().origin_length_sq())
    13
    """
    return v
