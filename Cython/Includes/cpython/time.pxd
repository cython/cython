"""
Cython implementation of (parts of) the standard library time module.
"""

from libc.stdint cimport int64_t
from cpython.exc cimport PyErr_SetFromErrno

cdef extern from "pytime.h":
    ctypedef int64_t _PyTime_t
    _PyTime_t _PyTime_GetSystemClock() nogil
    double _PyTime_AsSecondsDouble(_PyTime_t t) nogil

from libc.time cimport (
    tm,
    time_t,
    localtime as libc_localtime,
)


cdef inline double time() nogil:
    cdef:
        _PyTime_t tic

    tic = _PyTime_GetSystemClock()
    return _PyTime_AsSecondsDouble(tic)


cdef inline tm localtime() nogil except *:
    """
    Analogue to the stdlib time.localtime.  The returned struct
    has some entries that the stdlib version does not: tm_gmtoff, tm_zone
    """
    cdef:
        time_t tic = <time_t>time()
        tm* result

    result = libc_localtime(&tic)
    if result is NULL:
        PyErr_SetFromErrno(RuntimeError)
        raise RuntimeError()  # Cython and the C compiler can't know that the above always raises.
    # Fix 0-based date values (and the 1900-based year).
    result.tm_year += 1900
    result.tm_mon += 1
    result.tm_wday += 1
    result.tm_yday += 1
    return result[0]
