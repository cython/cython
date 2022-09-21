# mode: run
# tag: cpp, cpp17, no-cpp-locals
# no cpp_locals because this test is already run with cpp_locals explicitly set

# cython: cpp_locals=True

cdef cppclass C:
    C()

cdef class PyC:
    """
    >>> PyC() and None  # doesn't really do anything, but should run
    """
    cdef C  # this limited usage wasn't triggering the creation of utility code
