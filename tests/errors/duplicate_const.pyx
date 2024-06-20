# mode: error

cdef extern from *:
    cdef const const int a
    cdef const volatile int b
    cdef volatile const int c
    cdef volatile volatile int d


_ERRORS = """
4:9: Duplicate 'const'
7:9: Duplicate 'volatile'
"""
