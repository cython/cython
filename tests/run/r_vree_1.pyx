__doc__ = """
    >>> test(0)
    0L
    >>> test(1)
    1L

    >>> import sys
    >>> sys.maxint + 1 > sys.maxint
    True
    >>> type(sys.maxint * 2 + 1) is long
    True

    >>> test(sys.maxint + 1)
    2147483648L
    >>> test(sys.maxint * 2 + 1)
    4294967295L
"""

def test(k):
    cdef unsigned long m
    m = k
    return m
