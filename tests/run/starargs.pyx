__doc__ = """
    >>> spam(1,2,3)
    >>> spam(1,2)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (2 given)
    >>> spam(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (4 given)
    >>> spam(1,2,3, a=1)
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> grail(1,2,3)
    >>> grail(1,2,3,4)
    >>> grail(1,2,3,4,5,6,7,8,9)
    >>> grail(1,2)
    Traceback (most recent call last):
    TypeError: function takes exactly 3 arguments (2 given)
    >>> grail(1,2,3, a=1)
    Traceback (most recent call last):
    TypeError: 'a' is an invalid keyword argument for this function

    >>> swallow(1,2,3)
    >>> swallow(1,2,3,4)
    Traceback (most recent call last):
    TypeError: function takes at most 3 positional arguments (4 given)
    >>> swallow(1,2,3, a=1, b=2)
    >>> swallow(1,2,3, x=1)
    Traceback (most recent call last):
    TypeError: keyword parameter 'x' was given by position and by name

    >>> creosote(1,2,3)
    >>> creosote(1,2,3,4)
    >>> creosote(1,2,3, a=1)
    >>> creosote(1,2,3,4, a=1, b=2)
    >>> creosote(1,2,3,4, x=1)
    Traceback (most recent call last):
    TypeError: keyword parameter 'x' was given by position and by name
"""

def spam(x, y, z):
    pass

def grail(x, y, z, *a):
    pass

def swallow(x, y, z, **k):
    pass

def creosote(x, y, z, *a, **k):
    pass
