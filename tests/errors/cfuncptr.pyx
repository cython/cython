# mode: error

cdef int exceptmaybeminus2(int bad) except ?-2:
    if bad:
        raise RuntimeError
    else:
        return 0

def fail_exceptmaybeminus2(bad):
    cdef int (*fptr_a)(int) except -2
    cdef int (*fptr_b)(int) except -1
    cdef int (*fptr_c)(int) except ?-1
    fptr_a = exceptmaybeminus2
    fptr_b = exceptmaybeminus2
    fptr_c = exceptmaybeminus2

cdef extern from *:
    # define this as extern since Cython converts internal "except*" to "except -1"
    cdef int exceptstar(int bad) except *

def fail_exceptmaybeminus2(bad):
    cdef int (*fptr_a)(int) # noexcept
    cdef int (*fptr_b)(int) except -1
    cdef int (*fptr_c)(int) except ?-1
    fptr_a = exceptstar
    fptr_b = exceptstar
    fptr_c = exceptstar

_ERRORS = """
13:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except -2'
14:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except -1'
15:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except? -1'
25:13: Cannot assign type 'int (int) except *' to 'int (*)(int)'
26:13: Cannot assign type 'int (int) except *' to 'int (*)(int) except -1'
27:13: Cannot assign type 'int (int) except *' to 'int (*)(int) except? -1'
"""
