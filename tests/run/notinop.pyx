__doc__ = u"""
    >>> f(1,[1,2,3])
    False
    >>> f(5,[1,2,3])
    True
    >>> f(2,(1,2,3))
    False

    >>> g(1,[1,2,3])
    0
    >>> g(5,[1,2,3])
    1
    >>> g(2,(1,2,3))
    0

    >>> h([1,2,3,4])
    False
    >>> h([1,3,4])
    True

    >>> j([1,2,3,4])
    0
    >>> j([1,3,4])
    1
"""

def f(a,b):
    result = a not in b
    return result

def g(a,b):
    cdef int result
    result = a not in b
    return result

def h(b):
    result = 2 not in b
    return result

def j(b):
    cdef int result
    result = 2 not in b
    return result
