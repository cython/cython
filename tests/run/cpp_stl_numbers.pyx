# mode: run
# tag: cpp20, cpp

from libcpp.numbers cimport pi, e


def test_pi():
    """
    >>> import math
    >>> test_pi() == math.pi
    True
    """
    return pi

def test_e():
    """
    >>> import math
    >>> test_e() == math.e
    True
    """
    return e
