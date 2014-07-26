# tag: posix
from libc.stdlib  cimport getenv
from posix.stdlib cimport setenv, unsetenv
from posix.time cimport *

def test_itimer(sec, usec):
    """
    >>> test_itimer(10, 2)
    (10, 2)
    """
    cdef itimerval t, gtime

    t.it_interval.tv_sec = sec
    t.it_interval.tv_usec = usec
    t.it_value.tv_sec = sec
    t.it_value.tv_usec = usec
    ret = setitimer(ITIMER_REAL, &t, NULL)
    assert ret == 0
    ret = getitimer(ITIMER_REAL, &gtime)
    assert ret == 0
    t.it_interval.tv_sec = 0
    t.it_interval.tv_usec = 0
    t.it_value.tv_sec = 0
    t.it_value.tv_usec = 0
    ret = setitimer(ITIMER_REAL, &t, NULL)
    return gtime.it_interval.tv_sec, gtime.it_interval.tv_usec

def test_gettimeofday():
    """
    >>> test_gettimeofday()
    """
    cdef timeval t
    ret = gettimeofday(&t, NULL)
    assert ret == 0

def test_time():
    """
    >>> test_time()
    """
    cdef time_t t1, t2
    t1 = time(NULL)
    assert t1 != 0
    t1 = time(&t2)
    assert t1 == t2

def test_mktime():
    """
tests/run/posix_time.pyx
    >>> test_mktime()  # doctest:+ELLIPSIS
    (986138177, ...'Sun Apr  1 15:16:17 2001\\n')
    """
    cdef tm t, gmt
    cdef time_t tt
    cdef char *ct
    cdef char *tz

    tz = getenv("TZ")
    setenv("TZ", "UTC", 1)
    tzset()
    t.tm_sec = 17
    t.tm_min = 16
    t.tm_hour = 15
    t.tm_year = 101
    t.tm_mon = 3
    t.tm_mday = 1
    t.tm_isdst = 0
    tt = mktime(&t)
    assert tt != -1
    ct = ctime(&tt)
    assert ct != NULL
    if tz:
        setenv("TZ", tz, 1)
    else:
        unsetenv("TZ")
    tzset()
    return tt, ct
