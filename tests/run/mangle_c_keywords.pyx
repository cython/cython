# Tests that illegal member and vtab entries are mangled.
cdef class A:
    """
    >>> a = A(100)
    >>> a.case()
    100
    """
    def __init__(self, value):
        self.switch = value
    cdef int switch
    cpdef case(self):
        return self.switch
