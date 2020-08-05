"""
Cython implementation of (parts of) the standard library time module.
"""

from libc.stdint cimport int64_t

ctypedef int64_t _PyTime_t

cdef extern from "pytime.h":
    _PyTime_t _PyTime_GetSystemClock() nogil
    double _PyTime_AsSecondsDouble(_PyTime_t t) nogil

from libc.time cimport (
    tm,
    time_t,
    localtime as libc_localtime,
)


cpdef inline double time() nogil:
    cdef:
        _PyTime_t tic
    tic = _PyTime_GetSystemClock()
    return _PyTime_AsSecondsDouble(tic)


cpdef tm localtime() nogil:
    """
    Analogue to the stdlib time.localtime.  The returned struct
    has some entries that the stdlib version does not: tm_gmtoff, tm_zone

    When called from python, this returns a dict instead of a struct.
    """
    cdef:
        time_t tic = <time_t>time()
        tm* result

    result = libc_localtime(&tic)
    return result[0]
