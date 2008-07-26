__doc__ = u"""
    >>> f(1)
    (1, 17)
    >>> g()
    1
"""

def f(x):
    cdef int y
    z = 42
    with nogil:
        y = 17
    z = x
    return z,y

def g():
    with nogil:
        h()
    return 1

cdef int h() nogil except -1:
    pass
