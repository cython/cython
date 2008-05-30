__doc__ = u"""
    >>> f(5, 7)
    29509034655744L

    >>> g(13, 4)
    32

    >>> h(56, 7)
    105.0
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"L", u"")

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
