# Internals of the "long" type (Python 2) or "int" type (Python 3).

extern from "Python.h":
    """
    #if PY_MAJOR_VERSION < 3
     #include "longintrepr.h"
    #endif
    """
    ctypedef u32 digit
    ctypedef i32 sdigit  # Python >= 2.7 only

    ctypedef class __builtin__.py_long [object PyLongObject]:
        cdef digit* ob_digit

    cdef py_long _PyLong_New(isize s)

    cdef i64 PyLong_SHIFT
    cdef digit PyLong_BASE
    cdef digit PyLong_MASK
