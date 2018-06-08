# mode: run
# tag: cpdef

# This also makes a nice benchmark for the cpdef method call dispatching code.

cdef class Ext:
    """
    >>> x = Ext()
    >>> x.rec(10)
    0
    """
    cpdef rec(self, int i):
        return 0 if i < 0 else self.rec(i-1)


class Py(Ext):
    """
    >>> p = Py()
    >>> p.rec(10)
    0
    """
    pass


class Slots(Ext):
    """
    >>> s = Slots()
    >>> s.rec(10)
    0
    """
    __slots__ = ()


class PyOverride(Ext):
    """
    >>> p = PyOverride()
    >>> p.rec(10)
    10
    5
    >>> p.rec(12)
    12
    11
    10
    5
    """
    def rec(self, i):
        print(i)
        return Ext.rec(self, i) if i > 10 else 5


class SlotsOverride(Ext):
    """
    >>> s = SlotsOverride()
    >>> s.rec(10)
    10
    6
    >>> s.rec(12)
    12
    11
    10
    6
    """
    __slots__ = ()
    def rec(self, i):
        print(i)
        return Ext.rec(self, i) if i > 10 else 6
