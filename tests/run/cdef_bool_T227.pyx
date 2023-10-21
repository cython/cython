# ticket: t227

from cpython.bool cimport bool

def foo(bool a):
    """
    >>> foo(true)
    True
    >>> foo(false)
    False
    >>> foo('abc') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return a == True

def call_cfoo(a):
    """
    >>> call_cfoo(true)
    True
    >>> call_cfoo(false)
    False
    >>> call_cfoo('abc') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    return cfoo(a)

cdef cfoo(bool a):
    return a == True
