__doc__ = u"""
    >>> class test(object): a = 1
    >>> t = test()

    >>> f(t, 'a')
    1
    >>> f(t, 'b')
    Traceback (most recent call last):
    AttributeError: 'test' object has no attribute 'b'

    >>> g(t, 'a', 2)
    1
    >>> g(t, 'b', 2)
    2

    >>> h(t, 'a', 2)
    1
    >>> h(t, 'b', 2)
    2
"""

def f(a, b):
    return getattr(a, b)

def g(a, b, c):
    return getattr3(a, b, c)

def h(a, b, c):
    return getattr(a, b, c)
