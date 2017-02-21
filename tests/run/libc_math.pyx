# mode: run

from libc.math cimport (M_E, M_LOG2E, M_LOG10E, M_LN2, M_LN10, M_PI, M_PI_2,
        M_PI_4, M_1_PI, M_2_PI, M_2_SQRTPI, M_SQRT2, M_SQRT1_2)
from libc.math cimport (acos, asin, atan, atan2, cos, sin, tan, cosh, sinh,
        tanh, acosh, asinh, atanh, exp, log, log10, pow, sqrt)
cimport libc.math as libc_math


def test_pi():
    """
    >>> import math
    >>> test_pi() == math.pi
    True
    """
    return M_PI


def test_renamed_constants(math):
    """
    >>> import math
    >>> test_renamed_constants(math)
    """
    assert libc_math.M_E == libc_math.e == math.e
    assert libc_math.M_PI == libc_math.pi == math.pi


def test_sin(x):
    """
    >>> test_sin(0)
    0.0
    >>> from math import sin
    >>> [sin(k) == test_sin(k) for k in range(10)]
    [True, True, True, True, True, True, True, True, True, True]
    """
    return sin(x)
