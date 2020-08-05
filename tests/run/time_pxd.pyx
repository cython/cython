import time

from cpython cimport time as ctime


def test_time():
    """
    >>> tic1, tic2, tic3 = test_time()
    >>> assert tic1 <= tic2 <= tic3
    """
    # check that ctime.time() matches time.time() to within call-time tolerance
    tic1 = time.time()
    tic2 = ctime.time()
    tic3 = time.time()

    return tic1, tic2, tic3


def test_localtime():
    """
    >>> ltp, ltc = test_localtime()
    >>> assert ltp.tm_year == ltc.tm_year
    >>> assert ltp.tm_mon == ltc.tm_mon
    >>> assert ltp.tm_mday == ltc.tm_mday
    >>> assert ltp.tm_hour == ltc.tm_hour
    >>> assert ltp.tm_min == ltc.tm_min
    >>> assert ltp.tm_sec == ltc.tm_sec
    >>> assert ltp.tm_wday == ltc.tm_wday
    >>> assert ltp.tm_yday == ltc.tm_yday
    >>> assert ltp.tm_isdst == ltc.tm_isdst
    """
    # Note: the tm_sec assertion may fail in corner cases when the time.localtime
    #  call is just before the end of a second and the ctime.localtime
    #  is just after.
    ltp = time.localtime()
    ltc = ctime.localtime()
    return ltp, ltc
