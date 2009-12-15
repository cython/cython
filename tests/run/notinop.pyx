def f(a,b):
    """
    >>> f(1,[1,2,3])
    False
    >>> f(5,[1,2,3])
    True
    >>> f(2,(1,2,3))
    False
    """
    result = a not in b
    return result

def g(a,b):
    """
    >>> g(1,[1,2,3])
    0
    >>> g(5,[1,2,3])
    1
    >>> g(2,(1,2,3))
    0
    """
    cdef int result
    result = a not in b
    return result

def h(b):
    """
    >>> h([1,2,3,4])
    False
    >>> h([1,3,4])
    True
    """
    result = 2 not in b
    return result

def j(b):
    """
    >>> j([1,2,3,4])
    0
    >>> j([1,3,4])
    1
    """
    cdef int result
    result = 2 not in b
    return result

def k(a):
    """
    >>> k(1)
    0
    >>> k(5)
    1
    """
    cdef int result = a not in [1,2,3,4]
    return result

def m(int a):
    """
    >>> m(2)
    0
    >>> m(5)
    1
    """
    cdef int result = a not in [1,2,3,4]
    return result

def n(a):
    """
    >>> n('d *')
    0
    >>> n('xxx')
    1
    """
    cdef int result = a.lower() not in [u'a *',u'b *',u'c *',u'd *']
    return result

def p(a):
    """
    >>> p('a')
    0
    >>> p(1)
    1
    """
    cdef dict d = {u'a': 1, u'b': 2}
    cdef int result = a not in d
    return result

def q(a):
    """
    >>> q(1)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    cdef dict d = None
    cdef int result = a not in d # should fail with a TypeError
    return result
