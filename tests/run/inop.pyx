__doc__ = u"""
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

    >>> k(1)
    1
    >>> k(5)
    0

    >>> m(2)
    1
    >>> m(5)
    0

    >>> n('d *')
    1
    >>> n('xxx')
    0

    >>> p(1)
    0
    >>> p('a')
    1

    >>> q(1)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable

    >>> l = [1,2,3,4]
    >>> l2 = [l[1:],l[:-1],l]
    >>> 2 in l in l2
    True
    >>> r(2)
    1
    >>> s(2)
    1
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

def k(a):
    cdef int result = a in [1,2,3,4]
    return result

def m(int a):
    cdef int result = a in [1,2,3,4]
    return result

def n(a):
    cdef int result = a.lower() in [u'a *',u'b *',u'c *',u'd *']
    return result

def p(a):
    cdef dict d = {u'a': 1, u'b': 2}
    cdef int result = a in d
    return result

def q(a):
    cdef dict d = None
    cdef int result = a in d # should fail with a TypeError
    return result

def r(a):
    l = [1,2,3,4]
    l2 = [l[1:],l[:-1],l]
    cdef int result = a in l in l2
    return result

def s(a):
    cdef int result = a in [1,2,3,4] in [[1,2,3],[2,3,4],[1,2,3,4]]
    return result
