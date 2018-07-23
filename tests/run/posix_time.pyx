# tag: posix

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
    return int(gtime.it_interval.tv_sec), int(gtime.it_interval.tv_usec)

def test_gettimeofday():
    """
    >>> test_gettimeofday()
    """
    cdef timeval t
    ret = gettimeofday(&t, NULL)
    assert ret == 0
