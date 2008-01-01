__doc__ = """
    >>> s = Silly(1,2,3, 'test')

    >>> s.spam(1,2,3)
    >>> s.spam(1,2)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (2 given)
    >>> s.spam(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (4 given)
    >>> s.spam(1,2,3, a=1)
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> s.grail(1,2,3)
    >>> s.grail(1,2,3,4)
    >>> s.grail(1,2,3,4,5,6,7,8,9)
    >>> s.grail(1,2)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (2 given)
    >>> s.grail(1,2,3, a=1)
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> s.swallow(1,2,3)
    >>> s.swallow(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)
    >>> s.swallow(1,2,3, a=1, b=2)
    >>> s.swallow(1,2,3, x=1)
    Traceback (most recent call last):
    TypeError: keyword parameter 'x' was given by position and by name

    >>> s.creosote(1,2,3)
    >>> s.creosote(1,2,3,4)
    >>> s.creosote(1,2,3, a=1)
    >>> s.creosote(1,2,3,4, a=1, b=2)
    >>> s.creosote(1,2,3,4, x=1)
    Traceback (most recent call last):
    TypeError: keyword parameter 'x' was given by position and by name
"""

cdef class Silly:

    def __init__(self, *a):
        pass

    def spam(self, x, y, z):
        pass
    
    def grail(self, x, y, z, *a):
        pass
    
    def swallow(self, x, y, z, **k):
        pass
    
    def creosote(self, x, y, z, *a, **k):
        pass
