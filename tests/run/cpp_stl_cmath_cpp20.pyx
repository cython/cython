# mode: run
# tag: cpp, werror, cpp20

from libcpp.cmath cimport lerp

def test_lerp(double a, double b, double t):
    """ Test C++20 std::lerp function
    >>> test_lerp(1.0, 2.0, 0.5)
    1.5
    >>> test_lerp(1.0, 4.0, 0.5)
    2.5
    """
    return lerp(a, b, t)
