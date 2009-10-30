def f(int a):
    """
    >>> f(5)
    5
    """
    cdef int i,j
    cdef int *p
    i = a
    p = &i
    j = p[0]
    return j
