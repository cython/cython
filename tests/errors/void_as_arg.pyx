cdef extern from *:
    void foo(void)

_ERRORS = u"""
2:13:Use spam() rather than spam(void) to declare a function with no arguments.
"""
