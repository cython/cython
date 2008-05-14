__doc__ = u"""
>>> f(100)
101L
>>> g(3000000000)
3000000001L
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"L", u"")

def f(x):
    cdef unsigned long long ull
    ull = x
    return ull + 1

def g(unsigned long x):
    return x + 1
