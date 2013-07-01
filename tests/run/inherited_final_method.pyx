# mode: run
# tag: exttype, final

cimport cython


cdef class BaseClass:
    """
    >>> obj = BaseClass()
    >>> obj.call_base()
    True
    """
    cdef method(self):
        return True

    def call_base(self):
        return self.method()


@cython.final
cdef class Child(BaseClass):
    """
    >>> obj = Child()
    >>> obj.call_base()
    True
    >>> obj.call_child()
    True
    """
    cdef method(self):
        return True

    def call_child(self):
        # original bug: this requires a proper cast for self
        return self.method()
