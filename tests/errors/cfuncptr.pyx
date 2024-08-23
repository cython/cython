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

    struct mystruct:
        int (*func_ptr)(int param) nogil
        void (*func_ptr_void)(int param) nogil

def fail_exceptstar(bad):
    cdef int (*fptr_a)(int) noexcept
    cdef int (*fptr_b)(int) except -1
    cdef int (*fptr_c)(int) except ?-1
    fptr_a = exceptstar
    fptr_b = exceptstar
    fptr_c = exceptstar

cdef int cb(int param) nogil:
    return param

cdef void cb_void(int param) except * nogil:
    return

def fail_struct_pointer():
    cdef mystruct ms = mystruct(&cb, &cb_void)


_ERRORS = """
13:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except -2'. Exception values are incompatible.
14:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except -1'. Exception values are incompatible.
15:13: Cannot assign type 'int (int) except? -2' to 'int (*)(int) except? -1'. Exception values are incompatible.
29:13: Cannot assign type 'int (int) except *' to 'int (*)(int) noexcept'. Exception values are incompatible. Suggest adding 'noexcept' to the type of 'exceptstar'.
30:13: Cannot assign type 'int (int) except *' to 'int (*)(int) except -1'. Exception values are incompatible.
31:13: Cannot assign type 'int (int) except *' to 'int (*)(int) except? -1'. Exception values are incompatible.
40:32: Cannot assign type 'int (*)(int) except? -1 nogil' to 'int (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to the type of the value being assigned.
40:32: Cannot assign type 'int (*)(int) except? -1 nogil' to 'int (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to the type of the value being assigned.
40:37: Cannot assign type 'void (*)(int) except * nogil' to 'void (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to the type of the value being assigned.
40:37: Cannot assign type 'void (*)(int) except * nogil' to 'void (*)(int) noexcept nogil'. Exception values are incompatible. Suggest adding 'noexcept' to the type of the value being assigned.
"""
