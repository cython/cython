# http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/time.h.html

from posix.signal cimport sigevent
from posix.types cimport clock_t, clockid_t, suseconds_t, time_t, timer_t

cdef extern from "sys/time.h" nogil:

    enum: CLOCKS_PER_SEC
    enum: CLOCK_PROCESS_CPUTIME_ID
    enum: CLOCK_THREAD_CPUTIME_ID

    enum: CLOCK_REALTIME
    enum: TIMER_ABSTIME
    enum: CLOCK_MONOTONIC

    # FreeBSD-specific clocks
    enum: CLOCK_UPTIME
    enum: CLOCK_UPTIME_PRECISE
    enum: CLOCK_UPTIME_FAST
    enum: CLOCK_REALTIME_PRECISE
    enum: CLOCK_REALTIME_FAST
    enum: CLOCK_MONOTONIC_PRECISE
    enum: CLOCK_MONOTONIC_FAST
    enum: CLOCK_SECOND

    # Linux-specific clocks
    enum: CLOCK_PROCESS_CPUTIME_ID
    enum: CLOCK_THREAD_CPUTIME_ID
    enum: CLOCK_MONOTONIC_RAW
    enum: CLOCK_REALTIME_COARSE
    enum: CLOCK_MONOTONIC_COARSE
    enum: CLOCK_BOOTTIME
    enum: CLOCK_REALTIME_ALARM
    enum: CLOCK_BOOTTIME_ALARM

    enum: ITIMER_REAL
    enum: ITIMER_VIRTUAL
    enum: ITIMER_PROF

    cdef struct timeval:
        time_t      tv_sec
        suseconds_t tv_usec

    cdef struct itimerval:
        timeval it_interval
        timeval it_value

    cdef struct timezone:
        int tz_minuteswest
        int dsttime

    cdef struct timespec:
        time_t tv_sec
        long   tv_nsec

    cdef struct itimerspec:
        timespec it_interval
        timespec it_value

    cdef struct tm:
        int  tm_sec
        int  tm_min
        int  tm_hour
        int  tm_mday
        int  tm_mon
        int  tm_year
        int  tm_wday
        int  tm_yday
        int  tm_isdst
        char *tm_zone
        long tm_gmtoff

    char    *asctime(const tm *)
    char    *asctime_r(const tm *, char *)
    clock_t clock()
    int     clock_getcpuclockid(pid_t, clockid_t *)
    int     clock_getres(clockid_t, timespec *)
    int     clock_gettime(clockid_t, timespec *)
    int     clock_nanosleep(clockid_t, int, const timespec *, timespec *)
    int     clock_settime(clockid_t, const timespec *)
    char    *ctime(const time_t *)
    char    *ctime_r(const time_t *, char *)
    double  difftime(time_t, time_t)
    tm      *getdate(const char *)
    int     getitimer(int, itimerval *)
    int     gettimeofday(timeval *tp, timezone *tzp)
    tm      *gmtime(const time_t *)
    tm      *gmtime_r(const time_t *, tm *)
    tm      *localtime(const time_t *)
    tm      *localtime_r(const time_t *, tm *)
    time_t  mktime(tm *)
    int     nanosleep(const timespec *, timespec *)
    int     setitimer(int, const itimerval *, itimerval *)
    size_t  strftime(char *, size_t, const char *, const tm *)
    char    *strptime(const char *, const char *, tm *)
    time_t  time(time_t *)
    int     timer_create(clockid_t, sigevent *, timer_t *)
    int     timer_delete(timer_t)
    int     timer_gettime(timer_t, itimerspec *)
    int     timer_getoverrun(timer_t)
    int     timer_settime(timer_t, int, const itimerspec *, itimerspec *)
    void    tzset()

    int daylight
    long timezone
    char *tzname[2]
