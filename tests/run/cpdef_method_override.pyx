# mode: run
# tag: cpdef
# ticket: 1771

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
    cpdef callmeth(self):
        return self.callmeth2()
    cpdef callmeth2(self):
        # not overridden by subclasses
        return self.meth()
    cpdef meth(self):
        # overridden by subclasses
        print("BaseType.meth")


class NonOverride(BaseType):
    """
    >>> NonOverride().callmeth()
    BaseType.meth
    >>> obj = NonOverride()
    >>> obj.callmeth()
    BaseType.meth
    >>> obj.callmeth()
    BaseType.meth
    >>> _call_method(NonOverride)
    BaseType.meth
    BaseType.meth
    BaseType.meth
    BaseType.meth
    BaseType.meth
    BaseType.meth
    """


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


class DynamicOverride(BaseType):
    """
    >>> DynamicOverride().callmeth()
    meth1
    >>> obj = DynamicOverride()
    >>> obj.callmeth()
    meth1
    >>> obj.callmeth()
    meth2
    >>> obj.callmeth()
    BaseType.meth
    >>> obj.callmeth()
    BaseType.meth
    >>> _call_method(DynamicOverride)
    meth1
    meth1
    meth2
    meth1
    meth2
    BaseType.meth
    """
    def __init__(self):
        self.meth = self.meth1
    def meth1(self):
        self.meth = self.meth2
        print("meth1")
    def meth2(self):
        del self.meth
        print("meth2")
