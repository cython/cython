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

    >>> k(1)
    0
    >>> k(5)
    1

    >>> m(2)
    0
    >>> m(5)
    1

    >>> n('d *')
    0
    >>> n('xxx')
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

def k(a):
    cdef int result = a not in [1,2,3,4]
    return result

def m(int a):
    cdef int result = a not in [1,2,3,4]
    return result

def n(a):
    cdef int result = a.lower() not in [u'a *',u'b *',u'c *',u'd *']
    return result
