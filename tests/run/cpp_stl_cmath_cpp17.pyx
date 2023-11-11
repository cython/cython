# mode: run
# tag: cpp, werror, cpp17

from libcpp.cmath cimport beta, legendre, hypot

def test_beta(double x, double y):
    """
    Test C++17 std::beta function
    >>> test_beta(1.0, 1.0)
    1.0
    >>> test_beta(1.0, 2.0)
    0.5
    """
    return beta(x, y)

def test_legendre(int x, double y):
    """
    Test C++17 std::legendre function
    >>> test_legendre(1, 0.5)
    0.5
    >>> test_legendre(2, 0.5)
    -0.125
    """
    return legendre(x, y)

def test_hypot(double x, double y, double z):
    """
    Test C++17 std::hypot function
    >>> test_hypot(1.0, 2.0, 2.0)
    3.0
    >>> test_hypot(3.0, 4.0, 0.0)
    5.0
    """
    return hypot(x, y, z)