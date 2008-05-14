__doc__ = u"""
    >>> f(5)
    5
"""

def f(int a):
    cdef int i,j
    cdef int *p
    i = a
    p = &i
    j = p[0]
    return j
