__doc__ = """
    >>> test(0)
    0L
    >>> test(1)
    1L
    >>> 2**36
    68719476736L
    >>> test(2**36)
    0L
    >>> test(2L**36)
    0L
"""

def test(k):
    cdef unsigned long m
    m = k
    return m
