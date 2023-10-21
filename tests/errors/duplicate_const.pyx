# mode: error

cdef extern from *:
    cdef const const i32 a
    cdef const volatile i32 b
    cdef volatile const i32 c
    cdef volatile volatile i32 d


_ERRORS = """
4:9: Duplicate 'const'
7:9: Duplicate 'volatile'
"""
