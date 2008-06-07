__doc__ = u"""
    >>> str(f(5, 7))
    '29509034655744'

    >>> g(13, 4)
    32

    >>> h(56, 7)
    105.0
"""

def f(a,b):
    a += b
    a *= b
    a **= b
    return a

def g(int a, int b):
    a -= b
    a /= b
    a <<= b
    return a

def h(double a, double b):
    a /= b
    a += b
    a *= b
    return a
