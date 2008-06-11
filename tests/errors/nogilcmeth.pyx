cdef class C:
    cdef void f(self):
        pass

_ERRORS = u"""
2:6: Signature does not match previous declaration
"""
