__doc__ = u"""
    >>> x = 1
    >>> for i in range(10):
    ...     x = x + i
    >>> x
    46

    >>> add_pyrange(10)
    46
    >>> add_py(10)
    46
    >>> add_c(10)
    46
"""

def add_pyrange(max):
    x = 1
    for i in range(max):
        x = x + i
    return x

def add_py(max):
    x = 1
    for i from 0 <= i < max:
        x = x + i
    return x

def add_c(max):
    cdef int x,i
    x = 1
    for i from 0 <= i < max:
        x = x + i
    return x
