# Internals of the "int" type.

cdef extern from "Python.h":
    ctypedef unsigned int digit
    ctypedef int sdigit

    ctypedef class __builtin__.py_long [object PyLongObject, check_size opaque_in_limited_api]:
        cdef digit* ob_digit

    cdef py_long _PyLong_New(Py_ssize_t s)

    cdef long PyLong_SHIFT
    cdef digit PyLong_BASE
    cdef digit PyLong_MASK
