# mode: error

cdef cdef_yield():
    def inner():
        pass

cpdef cpdef_yield():
    def inner():
        pass

_ERRORS = u"""
3:5: closures inside cdef functions not yet supported
7:6: closures inside cdef functions not yet supported
"""
