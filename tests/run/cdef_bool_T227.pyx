__doc__ = u"""
>>> foo(True)
True
>>> foo(False)
False
>>> foo('abc') # doctest: +ELLIPSIS
Traceback (most recent call last):
TypeError: ...

>>> call_cfoo(True)
True
>>> call_cfoo(False)
False
>>> call_cfoo('abc') # doctest: +ELLIPSIS
Traceback (most recent call last):
TypeError: ...
"""

def foo(bool a):
    return a == True

def call_cfoo(a):
    return cfoo(a)

cdef cfoo(bool a):
    return a == True
