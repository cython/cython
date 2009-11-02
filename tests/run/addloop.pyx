__doc__ = u"""
    >>> x = 1
    >>> for i in range(10):
    ...     x = x + i
    >>> x
    46

"""

def add_pyrange(max):
    """
    >>> add_pyrange(10)
    46
    """
    x = 1
    for i in range(max):
        x = x + i
    return x

def add_py(max):
    """
    >>> add_py(10)
    46
    """
    x = 1
    for i from 0 <= i < max:
        x = x + i
    return x

def add_c(max):
    """
    >>> add_c(10)
    46
    """
    cdef int x,i
    x = 1
    for i from 0 <= i < max:
        x = x + i
    return x
