__doc__ = u"""
__getattribute__ and __getattr__ special methods for a single class.

    >>> a = just_getattribute()
    >>> a.bar
    'bar'
    >>> a.invalid
    Traceback (most recent call last):
    AttributeError

    >>> a = just_getattr()
    >>> a.foo
    10
    >>> a.bar
    'bar'
    >>> a.invalid
    Traceback (most recent call last):
    AttributeError

    >>> a = both()
    >>> a.foo
    10
    >>> a.bar
    'bar'
    >>> a.invalid
    Traceback (most recent call last):
    AttributeError
"""

cdef class just_getattribute:
    def __getattribute__(self,n):
        if n == u'bar':
            return n
        else:
            raise AttributeError

cdef class just_getattr:
    cdef readonly int foo
    def __init__(self):
        self.foo = 10
    def __getattr__(self,n):
        if n == u'bar':
            return n
        else:
            raise AttributeError

cdef class both:
    cdef readonly int foo
    def __init__(self):
        self.foo = 10
    def __getattribute__(self,n):
        if n == u'foo':
            return self.foo
        else:
            raise AttributeError
    def __getattr__(self,n):
        if n == u'bar':
            return n
        else:
            raise AttributeError
