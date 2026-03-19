# mode: compile
# cython: test_fail_if_c_code_has = CythonPyMutexPublicCheck

cimport cython

# PyMutex is not in a pxd file, so no need to generate Stable ABI sanity check

cdef class C:
    cdef cython.pymutex l
