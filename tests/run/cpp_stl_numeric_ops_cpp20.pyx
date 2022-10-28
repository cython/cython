# mode: run
# tag: cpp, werror, cpp20

from libcpp.numeric cimport midpoint

def test_midpoint_integer(int a, int b):
    """
    Test midpoint for integer types
    >>> test_midpoint_integer(2, 6)
    4
    """
    cdef int res = midpoint[int](a, b)
    return res


def test_midpoint_float(float a, float b):
    """
    Test midpoint for float
    >>> test_midpoint_float(2, 6)
    4.0
    """
    cdef float res = midpoint[float](a, b)
    return res
