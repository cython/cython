__doc__ = u"""
    >>> f(1.0, 2.95)[0] == f(1.0, 2.95)[1]
    True

    >>> g(4)
    1024

    >>> h(4)
    625

    >>> constant_py() == 2 ** 10
    True

    >>> constant_long() == 2 ** 36
    True
    
    >>> small_int_pow(3)
    (1, 3, 9, 27, 81)
    >>> small_int_pow(-5)
    (1, -5, 25, -125, 625)
    
    >>> int_pow(7, 2)
    49
    >>> int_pow(5, 3)
    125
    >>> int_pow(2, 10)
    1024
"""

def f(obj2, obj3):
    cdef float flt1, flt2, flt3
    flt2, flt3 = obj2, obj3

    flt1 = flt2 ** flt3
    obj1 = obj2 ** obj3
    return flt1, obj1

def g(i):
    return i ** 5

def h(i):
    return 5 ** i

def constant_py():
    result = (<object>2) ** 10
    return result

def constant_long():
    result = (<object>2L) ** 36
    return result

def small_int_pow(long s):
    return s**0, s**1, s**2, s**3, s**4

def int_pow(short a, short b):
    return a**b
