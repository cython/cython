# ticket: t227

from cpython.bool cimport bool

def foo(bool a):
    """
    >>> foo(True)
    True
    >>> foo(False)
    False
    >>> foo('abc') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return a == True

def call_cfoo(a):
    """
    >>> call_cfoo(True)
    True
    >>> call_cfoo(False)
    False
    >>> call_cfoo('abc') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return cfoo(a)

cdef cfoo(bool a):
    return a == True
