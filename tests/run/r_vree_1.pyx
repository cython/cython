import sys
if sys.version_info[0] < 3:
    __doc__ = u"""

    >>> test(0)
    0L
    >>> test(1)
    1L

    >>> sys.maxint + 1 > sys.maxint
    True
    >>> type(sys.maxint * 2 + 1) is long
    True

    >>> test(sys.maxint + 1) == sys.maxint + 1
    True
    >>> test(sys.maxint * 2 + 1) == sys.maxint * 2 + 1
    True

    >>> test(256 ** unsigned_long_size() - 1) > 0
    True
    >>> test(256 ** unsigned_long_size() - 1) > sys.maxint
    True
    """
else:
    __doc__ = u"""
    >>> test(0)
    0
    >>> test(1)
    1
    >>> test(256 ** unsigned_long_size() - 1) > 0
    True
    """

def test(k):
    cdef unsigned long m
    m = k
    return m

def unsigned_long_size():
    return sizeof(unsigned long)
