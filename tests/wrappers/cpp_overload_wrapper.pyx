# tag: cpp

cimport cpp_overload_wrapper_lib as cppwrap_lib

cdef class DoubleKeeper:
    """
    >>> d = DoubleKeeper()
    >>> d.get_number()
    1.0
    >>> d.set_number(5.5)
    >>> d.get_number()
    5.5
    >>> d.set_number(0)
    >>> d.get_number()
    0.0
    """
    cdef cppwrap_lib.DoubleKeeper* keeper

    def __cinit__(self, number=None):
        if number is None:
            self.keeper = new cppwrap_lib.DoubleKeeper()
        else:
            self.keeper = new cppwrap_lib.DoubleKeeper(number)

    def __dealloc__(self):
        del self.keeper

    def set_number(self, number=None):
        if number is None:
            self.keeper.set_number()
        else:
            self.keeper.set_number(number)

    def get_number(self):
        return self.keeper.get_number()

    def transmogrify(self, double value):
        """
        >>> d = DoubleKeeper(5.5)
        >>> d.transmogrify(1.0)
        5.5
        >>> d.transmogrify(2.0)
        11.0
        """
        return self.keeper.transmogrify(value)


def voidfunc():
    """
    >>> voidfunc()
    """
    cppwrap_lib.voidfunc()

def doublefunc(double x, double y, double z):
    """
    >>> doublefunc(1.0, 2.0, 3.0) == 1.0 + 2.0 + 3.0
    True
    """
    return cppwrap_lib.doublefunc(x, y, z)

def transmogrify_from_cpp(DoubleKeeper obj not None, double value):
    """
    >>> d = DoubleKeeper(2.0)
    >>> d.transmogrify(3.0) == 6.0
    True
    """
    return cppwrap_lib.transmogrify_from_cpp(obj.keeper, value)
