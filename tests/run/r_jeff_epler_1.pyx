__doc__ = u"""
    >>> blowup([2, 3, 5])
    1
"""

def blowup(p):
    cdef int n, i
    n = 10
    i = 1
    return n % p[i]
