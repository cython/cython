# Copied from cdef_multiple_inheritance.pyx
# but with __slots__ and without __dict__

cdef class CBase(object):
    cdef int a
    cdef c_method(self):
        return "CBase"
    cpdef cpdef_method(self):
        return "CBase"

class PyBase(object):
    __slots__ = []
    def py_method(self):
        return "PyBase"

cdef class Both(CBase, PyBase):
    """
    >>> b = Both()
    >>> b.py_method()
    'PyBase'
    >>> b.cp_method()
    'Both'
    >>> b.call_c_method()
    'Both'

    >>> isinstance(b, CBase)
    True
    >>> isinstance(b, PyBase)
    True
    """
    cdef c_method(self):
        return "Both"
    cpdef cp_method(self):
        return "Both"
    def call_c_method(self):
        return self.c_method()

cdef class BothSub(Both):
    """
    >>> b = BothSub()
    >>> b.py_method()
    'PyBase'
    >>> b.cp_method()
    'Both'
    >>> b.call_c_method()
    'Both'
    """
    pass
