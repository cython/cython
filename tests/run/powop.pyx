__doc__ = u"""
    >>> f(1.0, 2.95)[0] == f(1.0, 2.95)[1]
    True

    >>> g(4)
    1024

    >>> h(4)
    625

    >>> constant_py() == 2L ** 10
    True

    >>> constant_long() == 2L ** 36
    True
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"2L", u"2")

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
