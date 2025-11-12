# mode: run
# tag: cpp, cpp20, no-cpp-locals

# cython: language_level=3

from libcpp.condition_variable cimport *
from libcpp.stop_token cimport stop_source
from libcpp.mutex cimport mutex, py_safe_construct_unique_lock
from libcpp cimport bool

import time
from threading import Thread

# Just minimal amounts of tests for the stop_token overrides for condition_variable_any

cdef extern from "<chrono>" namespace "std::chrono" nogil:
    cdef cppclass days:
        days()
        days(long)
    cdef cppclass milliseconds:
        milliseconds()
        milliseconds(long)

cdef extern from *:
    """
    namespace {
        auto get_time_point() {
            return std::chrono::steady_clock::now() + std::chrono::days(1);
        }

        using time_point_type = decltype(get_time_point());
    }
    """
    cdef cppclass time_point_type:
        pass

    time_point_type get_time_point()


cdef bool dummy_predicate() noexcept nogil:
    return False

def test_cv_any_stop_token1():
    """
    >>> test_cv_any_stop_token1()
    False
    """
    cdef mutex m
    cdef condition_variable_any cv
    cdef stop_source ss
    ss.request_stop()

    # no need to worry about the GIL because there's no other threads involved
    m.lock()
    try:
        # cv will instantly return because the stop has been requested
        result = cv.wait(m, ss.get_token(), dummy_predicate)
    finally:
        m.unlock()

    return result

def test_cv_any_stop_token2():
    """
    >>> test_cv_any_stop_token2()
    False
    """
    cdef mutex m
    cdef condition_variable_any cv
    cdef stop_source ss
    cdef stop_token st = ss.get_token()
    ss.request_stop()

    # no need to worry about the GIL because there's no other threads involved
    m.lock()
    try:
        # cv will instantly return because the stop has been requested
        result = cv.wait_for(m, ss.get_token(), days(10), dummy_predicate)
    finally:
        m.unlock()

    return result

def test_cv_any_stop_token3():
    """
    >>> test_cv_any_stop_token3()
    False
    """
    cdef mutex m
    cdef condition_variable_any cv
    cdef stop_source ss
    cdef stop_token st = ss.get_token()
    ss.request_stop()

    # no need to worry about the GIL because there's no other threads involved
    m.lock()
    try:
        # cv will instantly return because the stop has been requested
        result = cv.wait_until(m, ss.get_token(), get_time_point(), dummy_predicate)
    finally:
        m.unlock()

    return result

def test_py_safe_wait_basic(sleep_for):
    """
    >>> test_py_safe_wait_basic(None)
    >>> test_py_safe_wait_basic(0.05)
    >>> test_py_safe_wait_basic(0.0)
    """
    cdef condition_variable_any cv
    cdef mutex m
    l = unique_lock[mutex](m)

    def trigger():
        # needs the GIL
        l2 = py_safe_construct_unique_lock(m)
        cv.notify_all()
        if sleep_for is not None:
            time.sleep(sleep_for)

    t = Thread(target=trigger)
    t.start()
    py_safe_wait(cv, l)
    t.join()

    # try wait_for (testing compilation, rather than timeout)
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_for(cv, l, milliseconds(50000))
    t.join()

    # try wait_until (testing compilation, rather than timeout)
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_until(cv, l, get_time_point())
    t.join()

def test_py_safe_wait_object(sleep_for):
    """
    >>> test_py_safe_wait_object(None)
    >>> test_py_safe_wait_object(0.05)
    >>> test_py_safe_wait_object(0.0)
    """
    cdef condition_variable_any cv
    cdef mutex m
    success = False
    l = unique_lock[mutex](m)

    import sys

    def predicate():
        # The condition variable will always call this with the lock held
        return success

    def trigger():
        nonlocal success
        # needs the GIL
        l2 = py_safe_construct_unique_lock(m)
        success = True
        cv.notify_all()
        if sleep_for is not None:
            time.sleep(sleep_for)

    t = Thread(target=trigger)
    t.start()
    py_safe_object_wait(cv, l, predicate)
    t.join()

    # try wait_for (testing compilation, rather than timeout)
    success = False
    t = Thread(target=trigger)
    t.start()
    py_safe_object_wait_for(cv, l, milliseconds(50000), predicate)
    t.join()

    # try wait_until (testing compilation, rather than timeout)
    success = False
    t = Thread(target=trigger)
    t.start()
    py_safe_object_wait_until(cv, l, get_time_point(), predicate)
    t.join()

    # Run again with stop token (only testing compilation here, not triggering the stop token)
    cdef stop_token st
    success = False
    t = Thread(target=trigger)
    t.start()
    py_safe_object_wait(cv, l, st, predicate)
    t.join()

    success = False
    t = Thread(target=trigger)
    t.start()
    py_safe_object_wait_for(cv, l, st, milliseconds(50000), predicate)
    t.join()

    success = False
    t = Thread(target=trigger)
    t.start()
    py_safe_object_wait_until(cv, l, st, get_time_point(), predicate)
    t.join()


cdef int global_value = 0

cdef bool global_value_predicate() noexcept nogil:
    return global_value > 0


def test_py_safe_wait_p(sleep_for):
    """
    >>> test_py_safe_wait_p(None)
    >>> test_py_safe_wait_p(0.05)
    >>> test_py_safe_wait_p(0.0)
    """
    global global_value
    global_value = 0

    cdef condition_variable_any cv
    cdef mutex m
    l = unique_lock[mutex](m)

    def trigger():
        global global_value
        # needs the GIL (for the sake of testing)
        l2 = py_safe_construct_unique_lock(m)
        global_value = 1
        cv.notify_all()
        if sleep_for is not None:
            time.sleep(sleep_for)

    t = Thread(target=trigger)
    t.start()
    py_safe_wait(cv, l, global_value_predicate)
    t.join()

    # Run again with stop token (only testing compilation here, not triggering the stop token)
    cdef stop_token st
    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait(cv, l, st, global_value_predicate)
    t.join()

    # try wait_for (testing compilation, rather than timeout)
    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_for(cv, l, milliseconds(50000), global_value_predicate)
    t.join()

    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_for(cv, l, st, milliseconds(50000), global_value_predicate)
    t.join()

    # try wait_until (testing compilation, rather than timeout)
    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_until(cv, l, get_time_point(), global_value_predicate)
    t.join()

    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_until(cv, l, st, get_time_point(), global_value_predicate)
    t.join()
