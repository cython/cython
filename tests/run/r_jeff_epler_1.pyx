def blowup(p):
    """
    >>> blowup([2, 3, 5])
    1
    """
    cdef int n, i
    n = 10
    i = 1
    return n % p[i]
