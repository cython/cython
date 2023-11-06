# ticket: t608

# This only works reliably in Python2. In Python3 ints are variable-sized.
# You get away with it for small ints but it's a bad idea

cdef class MyInt(int):
    """
    >>> MyInt(2) == 2
    True
    >>> MyInt(2).attr is None
    True
    """
    cdef readonly object attr

cdef class MyInt2(int):
    """
    >>> MyInt2(2) == 2
    True
    >>> MyInt2(2).attr is None
    True
    >>> MyInt2(2).test(3)
    5
    """
    cdef readonly object attr

    def test(self, arg):
        return self._test(arg)

    cdef _test(self, arg):
        return self + arg

cdef class MyInt3(MyInt2):
    """
    >>> MyInt3(2) == 2
    True
    >>> MyInt3(2).attr is None
    True
    >>> MyInt3(2).test(3)
    6
    """
    cdef _test(self, arg):
        return self + arg + 1
