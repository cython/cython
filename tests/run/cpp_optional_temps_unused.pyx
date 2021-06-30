# mode: run
# tag: cpp, cpp17

# cython: cpp_locals=True

cdef cppclass C:
    C()

cdef class PyC:
    """
    >>> PyC() and None  # doesn't really do anything, but should run
    """
    cdef C  # this limited usage wasn't triggering the creation of utility code
