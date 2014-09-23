# http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/time.h.html

from posix.types cimport suseconds_t, time_t

cdef extern from "sys/time.h" nogil:

    enum: ITIMER_REAL
    enum: ITIMER_VIRTUAL
    enum: ITIMER_PROF

    cdef struct timezone:
        int tz_minuteswest
        int dsttime

    cdef struct timeval:
        time_t      tv_sec
        suseconds_t tv_usec

    cdef struct itimerval:
        timeval it_interval
        timeval it_value

    int     getitimer(int, itimerval *)
    int     gettimeofday(timeval *tp, timezone *tzp)
    int     setitimer(int, const itimerval *, itimerval *)
