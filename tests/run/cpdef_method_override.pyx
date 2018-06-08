# mode: run
# tag: cpdef
# ticket: gh-1771

cdef class BaseType:
    """
    >>> BaseType().callmeth()
    BaseType.meth
    """
    def callmeth(self):
        return self.meth()
    cpdef meth(self):
        print("BaseType.meth")


class PyClass(BaseType):
    """
    >>> PyClass().callmeth()
    PyClass.meth
    """
    def meth(self):
        print("PyClass.meth")


class PySlotsClass(BaseType):
    """
    >>> PySlotsClass().callmeth()
    PySlotsClass.meth
    """
    __slots__ = []

    def meth(self):
        print("PySlotsClass.meth")
