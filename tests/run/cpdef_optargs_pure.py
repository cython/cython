# mode: run
# tag: cyfunction
# cython: binding=True

import cython


class PyClass(object):
    a = 2


class PyClass99(object):
    a = 99

    def pymethod(self, x, y=1, z=PyClass):
        """
        >>> obj = PyClass99()
        >>> obj.pymethod(0)
        (0, 1, 2)
        """
        return x, y, z.a


def func(x, y=1, z=PyClass):
    """
    >>> func(0)
    (0, 1, 2)
    >>> func(0, 3)
    (0, 3, 2)
    >>> func(0, 3, PyClass)
    (0, 3, 2)
    >>> func(0, 3, 5)
    Traceback (most recent call last):
    AttributeError: 'int' object has no attribute 'a'
    """
    return x, y, z.a


@cython.ccall
def pyfunc(x, y=1, z=PyClass):
    """
    >>> pyfunc(0)
    (0, 1, 2)
    >>> pyfunc(0, 3)
    (0, 3, 2)
    >>> pyfunc(0, 3, PyClass)
    (0, 3, 2)
    >>> pyfunc(0, 3, 5)
    Traceback (most recent call last):
    AttributeError: 'int' object has no attribute 'a'
    """
    return x, y, z.a
