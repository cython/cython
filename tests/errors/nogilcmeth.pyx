# mode: error

cdef class C:
    fn void f(self):
        pass

_ERRORS = u"""
2:13: Previous declaration is here
4:4: Signature not compatible with previous declaration
"""
