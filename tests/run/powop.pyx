__doc__ = """
    >>> f(1.0, 2.95)[0] == f(1.0, 2.95)[1]
    True

    >>> constant_py()
    1024L

    >>> constant_long() == 2L ** 36
    True
"""

def f(obj2, obj3):
    cdef float flt1, flt2, flt3
    flt2, flt3 = obj2, obj3

    flt1 = flt2 ** flt3
    obj1 = obj2 ** obj3
    return flt1, obj1

def constant_py():
    result = 2L ** 10
    return result

def constant_long():
    result = 2L ** 36
    return result
