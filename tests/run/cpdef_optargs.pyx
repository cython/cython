# mode: run
# tag: cyfunction
# cython: binding=True

cimport cython


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


cdef class CyClass:
    cpdef cpmethod(self, x, y=1, z=PyClass):
        """
        >>> obj = CyClass()
        >>> obj.cpmethod(0)
        (0, 1, 2)
        >>> obj.cpmethod(0, 3)
        (0, 3, 2)
        >>> obj.cpmethod(0, 3, PyClass)
        (0, 3, 2)
        >>> obj.cpmethod(0, 3, 5)
        Traceback (most recent call last):
        AttributeError: 'int' object has no attribute 'a'
        """
        return x, y, z.a

    y_value = 3
    p_class = PyClass

    cpdef cpmethod2(self, x, y=y_value, z=p_class):
        """
        >>> obj = CyClass()
        >>> obj.cpmethod2(0)
        (0, 3, 2)
        """
        return x, y, z.a

    def pymethod(self, x, y=y_value, z=p_class):
        """
        >>> obj = CyClass()
        >>> obj.pymethod(0)
        (0, 3, 2)
        """
        return x, y, z.a

    # change values to check that defaults above stay unmodified
    y_value = 98
    p_class = PyClass99


cpdef func(x, y=1, z=PyClass):
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
