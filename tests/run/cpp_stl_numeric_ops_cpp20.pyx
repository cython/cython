# mode: run
# tag: cpp, werror, cpp20

from libcpp.numeric cimport midpoint

def test_midpoint_integer(i32 a, i32 b):
    """
    Test midpoint for integer types
    >>> test_midpoint_integer(2, 6)
    4
    """
    let i32 res = midpoint[int](a, b)
    return res


def test_midpoint_float(f32 a, f32 b):
    """
    Test midpoint for float
    >>> test_midpoint_float(2, 6)
    4.0
    """
    let f32 res = midpoint[float](a, b)
    return res
