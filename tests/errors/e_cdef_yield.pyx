# mode: error

cdef cdef_yield():
    yield

cpdef cpdef_yield():
    yield

_ERRORS = u"""
4:4: 'yield' not supported here
7:4: 'yield' not supported here
"""
