def f(a, b, int i):
    """
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
    """
    assert a
    assert a+b
    assert i

def g(a, b):
    """
    >>> g(1, "works")
    >>> g(0, "fails")
    Traceback (most recent call last):
    AssertionError: fails
    """
    assert a, b
