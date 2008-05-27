__doc__ = u"""
    >>> f(1, 2, 1)
    >>> f(0, 2, 1)
    Traceback (most recent call last):
    AssertionError
    >>> f(1, -1, 1)
    Traceback (most recent call last):
    AssertionError
    >>> f(1, 2, 0)
    Traceback (most recent call last):
    AssertionError

    >>> g(1, "works")
    >>> g(0, "fails")
    Traceback (most recent call last):
    AssertionError: fails
"""

def f(a, b, int i):
    assert a
    assert a+b
    assert i

def g(a, b):
    assert a, b
