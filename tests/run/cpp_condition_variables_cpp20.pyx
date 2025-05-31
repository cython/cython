# mode: run
# tag: cpp, cpp20, no-cpp-locals

# cython: language_level=3

from libcpp.condition_variable cimport *
from libcpp.stop_token cimport stop_source
from libcpp.mutex cimport mutex
from libcpp cimport bool
from libcpp.utility cimport move

# Just minimal amounts of tests for the stop_token overrides for condition_variable_any

cdef extern from "<chrono>" namespace "std::chrono" nogil:
    cdef cppclass days:
        days()
        days(long)
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
