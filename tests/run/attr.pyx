__doc__ = """
    >>> class Test:
    ...     def __init__(self, i):
    ...         self.i = i
    >>> b = Test(1)
    >>> b.spam = Test(2)
    >>> b.spam.eggs = Test(3)
    >>> b.spam.eggs.spam = Test(4)
    >>> b.spam.eggs.spam.eggs = Test(5)

    >>> a = f(b)
    >>> print a.i
    2
    >>> print b.i
    1
    >>> print a.spam.i
    1
    >>> print b.spam.i
    2
    >>> print a.spam.eggs.i
    Traceback (most recent call last):
    AttributeError: Test instance has no attribute 'eggs'
    >>> print b.spam.eggs.i
    3
    >>> print a.spam.spam.i
    2
    >>> print b.spam.spam.i
    1
    >>> print a.spam.eggs.spam.i
    Traceback (most recent call last):
    AttributeError: Test instance has no attribute 'eggs'
    >>> print b.spam.eggs.spam.i
    4

    >>> a = g(b)
    >>> print a.i
    3
    >>> print b.i
    1
    >>> print a.spam.i
    4
    >>> print b.spam.i
    2
    >>> print a.spam.eggs.i
    1
    >>> print b.spam.eggs.i
    3
    >>> print a.spam.spam.i
    Traceback (most recent call last):
    AttributeError: Test instance has no attribute 'spam'
    >>> print b.spam.spam.i
    1
    >>> print a.spam.eggs.spam.i
    2
    >>> print b.spam.eggs.spam.i
    4
"""

def f(b):
    a = b.spam
    a.spam = b
    return a

def g(b):
    a = b.spam.eggs
    a.spam.eggs = b
    return a
