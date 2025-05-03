# mode: compile
# cython: test_assert_c_code_has = CythonPyMutexPublicCheck

# Because this file uses PyMutex in a pxd file, it must generate the CythonPyMutexPublicCheck sanity
# check for the Stable ABI

cdef class C:
    pass  # see pxd file
