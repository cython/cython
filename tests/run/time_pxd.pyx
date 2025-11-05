# mode: run
# tag: py3only,pytime

import time

from cpython cimport time as ctime

import sys
cdef bint IS_PYPY = hasattr(sys, 'pypy_version_info')


def test_time():
    """
    >>> tic1, tic2, tic3 = test_time()
    >>> tic1 <= tic3  or  (tic1, tic3)  # sanity check
    True
    >>> tic1 <= tic2  or  (tic1, tic2)
    True
    >>> tic2 <= tic3  or  (tic2, tic3)
    True
    """
    # check that C-API matches Py-API to within call-time tolerance
    tic1 = time.time()
    tic2 = ctime.time()
    tic3 = time.time()

    return tic1, tic2, tic3


def test_time_ns():
    """
    >>> tic1, tic2, tic3 = test_time_ns()
    >>> tic1 <= tic3  or  (tic1, tic3)  # sanity check
    True
    >>> tic1 <= tic2  or  (tic1, tic2)
    True
    >>> tic2 <= tic3  or  (tic2, tic3)
    True
    """
    # check that C-API matches Py-API to within call-time tolerance
    tic1 = time.time_ns()
    tic2 = ctime.time_ns()
    tic3 = time.time_ns()

    return tic1, tic2, tic3


def test_perf_counter():
    """
    >>> tic1, tic2, tic3 = test_perf_counter()
    >>> tic1 <= tic3  or  (tic1, tic3)  # sanity check
    True
    >>> tic1 <= tic2  or  (tic1, tic2)
    True
    >>> tic2 <= tic3  or  (tic2, tic3)
    True
    """
    # check that C-API matches Py-API to within call-time tolerance
    tic1 = time.perf_counter()  if not IS_PYPY else  ctime.perf_counter()
    tic2 = ctime.perf_counter()
    tic3 = time.perf_counter()  if not IS_PYPY else  ctime.perf_counter()

    return tic1, tic2, tic3


def test_perf_counter_ns():
    """
    >>> tic1, tic2, tic3 = test_perf_counter_ns()
    >>> tic1 <= tic3  or  (tic1, tic3)  # sanity check
    True
    >>> tic1 <= tic2  or  (tic1, tic2)
    True
    >>> tic2 <= tic3  or  (tic2, tic3)
    True
    """
    # check that C-API matches Py-API to within call-time tolerance
    tic1 = time.perf_counter_ns()  if not IS_PYPY else  ctime.perf_counter_ns()
    tic2 = ctime.perf_counter_ns()
    tic3 = time.perf_counter_ns()  if not IS_PYPY else  ctime.perf_counter_ns()

    return tic1, tic2, tic3


def test_monotonic():
    """
    >>> tic1, tic2, tic3 = test_monotonic()
    >>> tic1 <= tic3  or  (tic1, tic3)  # sanity check
    True
    >>> tic1 <= tic2  or  (tic1, tic2)
    True
    >>> tic2 <= tic3  or  (tic2, tic3)
    True
    """
    # check that C-API matches Py-API to within call-time tolerance
    tic1 = time.monotonic()  if not IS_PYPY else  ctime.monotonic()
    tic2 = ctime.monotonic()
    tic3 = time.monotonic()  if not IS_PYPY else  ctime.monotonic()

    return tic1, tic2, tic3


def test_monotonic_ns():
    """
    >>> tic1, tic2, tic3 = test_monotonic_ns()
    >>> tic1 <= tic3  or  (tic1, tic3)  # sanity check
    True
    >>> tic1 <= tic2  or  (tic1, tic2)
    True
    >>> tic2 <= tic3  or  (tic2, tic3)
    True
    """
    # check that C-API matches Py-API to within call-time tolerance
    tic1 = time.monotonic_ns()  if not IS_PYPY else  ctime.monotonic_ns()
    tic2 = ctime.monotonic_ns()
    tic3 = time.monotonic_ns()  if not IS_PYPY else  ctime.monotonic_ns()

    return tic1, tic2, tic3


def test_localtime():
    """
    >>> ltp, ltc = test_localtime()
    >>> ltp.tm_year == ltc['tm_year']  or  (ltp.tm_year, ltc['tm_year'])
    True
    >>> ltp.tm_mon == ltc['tm_mon']  or  (ltp.tm_mon, ltc['tm_mon'])
    True
    >>> ltp.tm_mday == ltc['tm_mday']  or  (ltp.tm_mday, ltc['tm_mday'])
    True
    >>> ltp.tm_hour == ltc['tm_hour']  or  (ltp.tm_hour, ltc['tm_hour'])
    True
    >>> ltp.tm_min == ltc['tm_min']  or  (ltp.tm_min, ltc['tm_min'])
    True
    >>> ltp.tm_sec == ltc['tm_sec']  or  (ltp.tm_sec, ltc['tm_sec'])
    True
    >>> ltp.tm_wday == ltc['tm_wday']  or (ltp.tm_wday, ltc['tm_wday'])
    True
    >>> ltp.tm_yday == ltc['tm_yday']  or  (ltp.tm_yday, ltc['tm_yday'])
    True
    >>> ltp.tm_isdst == ltc['tm_isdst']  or  (ltp.tm_isdst, ltc['tm_isdst'])
    True
    """
    ltp = time.localtime()
    ltc = ctime.localtime()

    i = 0
    while ltp.tm_sec != ltc.tm_sec:
        # If the time.localtime call is just before the end of a second and the
        #  ctime.localtime call is just after the beginning of the next second,
        #  re-call.  This should not occur twice in a row.
        time.sleep(0.1)
        ltp = time.localtime()
        ltc = ctime.localtime()
        i += 1
        if i > 10:
            break

    return ltp, ltc
