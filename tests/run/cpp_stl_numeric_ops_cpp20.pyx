# mode: run
# tag: cpp, werror, cpp20

from libcpp.numeric cimport midpoint, lerp

def test_midpoint_integer(int a, int b)
    """
    Test midpoint for integer types
    >>> test_midpoint_integer(2, 6)
    4
    """
    return midpoint[int](a, b)


def test_midpoint_float(float a, float b)
    """
    Test midpoint for float
    >>> test_midpoint_float(2, 6)
    3.35
    """
    return midpoint[float](a, b)

def test_lerp(float a, float b, float t)
    """
    Test lerp for float
    >>> test_lerp(1.0, 2.0, 0.5)
    1.5
    """
    return lerp[float](a, b, t)
