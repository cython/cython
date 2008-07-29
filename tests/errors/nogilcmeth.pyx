cdef class C:
    cdef void f(self):
        pass

_ERRORS = u"""
nogilcmeth.pyx:2:9: Signature not compatible with previous declaration
nogilcmeth.pxd:2:15: Previous declaration is here
"""
