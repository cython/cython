__doc__ = u"""
    >>> class Test(object):
    ...     def __init__(self, i):
    ...         self.i = i
    >>> b = Test(1)
    >>> b.spam = Test(2)
    >>> b.spam.eggs = Test(3)
    >>> b.spam.eggs.spam = Test(4)
    >>> b.spam.eggs.spam.eggs = Test(5)

    >>> a = f(b)
    >>> a.i
    2
    >>> b.i
    1
    >>> a.spam.i
    1
    >>> b.spam.i
    2
    >>> a.spam.eggs.i
    Traceback (most recent call last):
    AttributeError: 'Test' object has no attribute 'eggs'
    >>> b.spam.eggs.i
    3
    >>> a.spam.spam.i
    2
    >>> b.spam.spam.i
    1
    >>> a.spam.eggs.spam.i
    Traceback (most recent call last):
    AttributeError: 'Test' object has no attribute 'eggs'
    >>> b.spam.eggs.spam.i
    4

    >>> a = g(b)
    >>> a.i
    3
    >>> b.i
    1
    >>> a.spam.i
    4
    >>> b.spam.i
    2
    >>> a.spam.eggs.i
    1
    >>> b.spam.eggs.i
    3
    >>> a.spam.spam.i
    Traceback (most recent call last):
    AttributeError: 'Test' object has no attribute 'spam'
    >>> b.spam.spam.i
    1
    >>> a.spam.eggs.spam.i
    2
    >>> b.spam.eggs.spam.i
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
