# cython: auto_cpdef=True
# mode: run
# tag: directive, auto_cpdef, closures

"""
Tests for auto_cpdef=True with various closure capture types.
Pure-Python (.py) mode — all functions here get promoted to cpdef/ccall.
"""

import cython
from cython import cclass, int as cint, float as cfloat, bint

# ---------------------------------------------------------------------------
# Module-level promoted functions with closure captures
# ---------------------------------------------------------------------------

@cython.test_assert_path_exists('//CFuncDefNode//LambdaNode')
def capture_int_local(n: cint):
    """
    >>> capture_int_local(5)
    5
    """
    return (lambda: n)()


@cython.test_assert_path_exists('//CFuncDefNode')
def capture_float_local(x: cfloat):
    """
    >>> abs(capture_float_local(1.5) - 1.5) < 1e-6
    True
    """
    return (lambda: x)()


@cython.test_assert_path_exists('//CFuncDefNode')
def capture_bint_local(flag: bint):
    """
    >>> capture_bint_local(True)
    True
    >>> capture_bint_local(False)
    False
    """
    return (lambda: flag)()


@cython.test_assert_path_exists('//CFuncDefNode')
def genexpr_any(values):
    """
    >>> genexpr_any([1, 2, 3])
    True
    >>> genexpr_any([-1, -2])
    False
    """
    return any(x > 0 for x in values)


@cython.test_assert_path_exists('//CFuncDefNode')
def genexpr_all(values):
    """
    >>> genexpr_all([1, 2, 3])
    True
    >>> genexpr_all([1, -2, 3])
    False
    """
    return all(x > 0 for x in values)


@cython.test_assert_path_exists('//CFuncDefNode')
def sorted_with_key(values):
    """
    >>> sorted_with_key([-3, 1, -2])
    [1, -2, -3]
    """
    return sorted(values, key=lambda x: abs(x))


@cython.test_assert_path_exists('//CFuncDefNode')
def map_with_lambda(values):
    """
    >>> list(map_with_lambda([1, 2, 3]))
    [2, 4, 6]
    """
    return map(lambda x: x * 2, values)


@cython.test_assert_path_exists('//CFuncDefNode')
def listcomp_promoted(values):
    """
    >>> listcomp_promoted([1, 2, 3])
    [1, 4, 9]
    """
    return [x * x for x in values]


# ---------------------------------------------------------------------------
# cclass methods with closure captures
# ---------------------------------------------------------------------------

@cclass
class MyClass:
    value: cint

    def __init__(self, v: cint) -> None:
        self.value = v

    @cython.test_assert_path_exists('//CFuncDefNode//LambdaNode')
    def capture_self_via_lambda(self):
        """
        >>> MyClass(10).capture_self_via_lambda()
        10
        """
        return (lambda: self.value)()

    @cython.test_assert_path_exists('//CFuncDefNode')
    def genexpr_method(self, n: cint):
        """
        >>> MyClass(3).genexpr_method(5)
        True
        """
        return any(x > self.value for x in range(n))

    @cython.test_assert_path_exists('//CFuncDefNode')
    def listcomp_method(self, n: cint):
        """
        >>> MyClass(2).listcomp_method(4)
        [0, 2, 4, 6]
        """
        return [x * self.value for x in range(n)]
