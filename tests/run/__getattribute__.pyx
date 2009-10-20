__doc__ = u"""
__getattribute__ and __getattr__ special methods for a single class.
"""

cdef class just_getattribute:
    """
    >>> a = just_getattribute()
    >>> a.bar
    'bar'
    >>> a.invalid
    Traceback (most recent call last):
    AttributeError
    """
    def __getattribute__(self,n):
        if n == 'bar':
            return n
        else:
            raise AttributeError

cdef class just_getattr:
    """
    >>> a = just_getattr()
    >>> a.foo
    10
    >>> a.bar
    'bar'
    >>> a.invalid
    Traceback (most recent call last):
    AttributeError
    """
    cdef readonly int foo
    def __init__(self):
        self.foo = 10
    def __getattr__(self,n):
        if n == 'bar':
            return n
        else:
            raise AttributeError

cdef class both:
    """
    >>> a = both()
    >>> a.foo
    10
    >>> a.bar
    'bar'
    >>> a.invalid
    Traceback (most recent call last):
    AttributeError
    """
    cdef readonly int foo
    def __init__(self):
        self.foo = 10
    def __getattribute__(self,n):
        if n == 'foo':
            return self.foo
        else:
            raise AttributeError
    def __getattr__(self,n):
        if n == 'bar':
            return n
        else:
            raise AttributeError
