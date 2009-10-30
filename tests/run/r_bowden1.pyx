import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"L", u"")

def f(x):
    """
    >>> f(100)
    101L
    """
    cdef unsigned long long ull
    ull = x
    return ull + 1

def g(unsigned long x):
    """
    >>> g(3000000000)
    3000000001L
    """
    return x + 1
