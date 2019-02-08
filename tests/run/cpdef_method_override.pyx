# mode: run
# tag: cpdef
# ticket: gh-1771

def _call_method(cls):
    obj = cls()
    obj.callmeth()
    obj = cls()
    obj.callmeth()
    obj.callmeth()
    obj = cls()
    obj.callmeth()
    obj.callmeth()
    obj.callmeth()


cdef class BaseType:
    """
    >>> BaseType().callmeth()
    BaseType.meth
    >>> obj = BaseType()
    >>> obj.callmeth()
    BaseType.meth
    >>> obj.callmeth()
    BaseType.meth
    >>> _call_method(BaseType)
    BaseType.meth
    BaseType.meth
    BaseType.meth
    BaseType.meth
    BaseType.meth
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
    >>> obj = PyClass()
    >>> obj.callmeth()
    PyClass.meth
    >>> obj.callmeth()
    PyClass.meth
    >>> obj.callmeth()
    PyClass.meth
    >>> _call_method(PyClass)
    PyClass.meth
    PyClass.meth
    PyClass.meth
    PyClass.meth
    PyClass.meth
    PyClass.meth
    """
    def meth(self):
        print("PyClass.meth")


class PySlotsClass(BaseType):
    """
    >>> PySlotsClass().callmeth()
    PySlotsClass.meth
    >>> obj = PySlotsClass()
    >>> obj.callmeth()
    PySlotsClass.meth
    >>> obj.callmeth()
    PySlotsClass.meth
    >>> obj.callmeth()
    PySlotsClass.meth
    >>> _call_method(PySlotsClass)
    PySlotsClass.meth
    PySlotsClass.meth
    PySlotsClass.meth
    PySlotsClass.meth
    PySlotsClass.meth
    PySlotsClass.meth
    """
    __slots__ = []

    def meth(self):
        print("PySlotsClass.meth")
