# tag: cpp

cimport cppwrap_lib

cdef class DoubleKeeper:
    """
    >>> d = DoubleKeeper(1.0)
    >>> d.get_number() == 1.0
    True
    >>> d.get_number() == 2.0
    False
    >>> d.set_number(2.0)
    >>> d.get_number() == 2.0
    True
    >>> d.transmogrify(3.0) == 6.0
    True
    """
    cdef cppwrap_lib.DoubleKeeper* keeper

    def __cinit__(self, double number):
        self.keeper = new cppwrap_lib.DoubleKeeper(number)

    def __dealloc__(self):
        del self.keeper

    def set_number(self, double number):
        self.keeper.set_number(number)

    def get_number(self):
        return self.keeper.get_number()

    def transmogrify(self, double value):
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
