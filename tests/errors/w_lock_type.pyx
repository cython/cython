# mode: compile
# tag: warnings

cimport cython

cdef void misuse_the_gil1() noexcept nogil:
    cdef cython.pymutex l
    with l:
        with gil:
            pass

cdef void misuse_the_gil2() noexcept nogil:
    cdef cython.pymutex l
    with l:
        a = 1
        with gil:
            pass

cdef void misuse_the_gil3() noexcept nogil:
    cdef cython.pythread_type_lock l
    with l:
        with gil:
            pass

_WARNINGS = """
9:13: Acquiring the GIL inside a cython.pymutex lock. To avoid potential deadlocks acquire the GIL first.
16:13: Acquiring the GIL inside a cython.pymutex lock. To avoid potential deadlocks acquire the GIL first.
22:13: Acquiring the GIL inside a cython.pythread_type_lock lock. To avoid potential deadlocks acquire the GIL first.
"""
