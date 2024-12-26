# mode: compile
# tag: warnings

cimport cython

cdef void misuse_the_gil() noexcept nogil:
    cdef cython.pymutex l
    with l:
        with gil:
            pass

_WARNINGS = """
9:13: Acquiring the GIL inside a cython.pymutex lock. To avoid potential deadlocks acquire the GIL first.
"""
