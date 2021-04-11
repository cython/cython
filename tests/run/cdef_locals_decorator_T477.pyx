# ticket: t477

import cython
@cython.locals(x=double)
cdef func(x):
    return x**2

@cython.locals(x=double)
cdef func_defval(x=0):
    return x**2

def test():
    """
    >>> isinstance(test(), float)
    True
    """
    return func(2)

def test_defval(x=None):
    """
    >>> test_defval()
    0.0
    >>> test_defval(1)
    1.0
    >>> test_defval(2.0)
    4.0
    """
    if x is None:
        return func_defval()
    else:
        return func_defval(x)
