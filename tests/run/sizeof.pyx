__doc__ = u"""
    >>> f()
"""

cdef struct Spam:
    char *grail

def f():
    cdef int i, j, k
    cdef char *p
    i = sizeof(p)
    i = sizeof(j + k)
    i = sizeof(int)
    i = sizeof(Spam)
