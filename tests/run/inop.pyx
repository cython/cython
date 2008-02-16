__doc__ = """
    >>> f(1,[1,2,3])
    True
    >>> f(5,[1,2,3])
    False
    >>> f(2,(1,2,3))
    True

    >>> g(1,[1,2,3])
    1
    >>> g(5,[1,2,3])
    0
    >>> g(2,(1,2,3))
    1

    >>> h([1,2,3,4])
    True
    >>> h([1,3,4])
    False

    >>> j([1,2,3,4])
    1
    >>> j([1,3,4])
    0
"""

def f(a,b):
    result = a in b
    return result

def g(a,b):
    cdef int result
    result = a in b
    return result

def h(b):
    result = 2 in b
    return result

def j(b):
    cdef int result
    result = 2 in b
    return result
