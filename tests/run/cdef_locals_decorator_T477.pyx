# ticket: 477

import cython
@cython.locals(x=double)
cdef func(x):
    return x**2

def test():
    """
    >>> isinstance(test(), float)
    True
    """
    return func(2)
