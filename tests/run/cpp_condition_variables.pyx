# mode: run
# tag: cpp, cpp11, no-cpp-locals
# Note - keep this file as cpp11 (and put cpp20 tests in a separate file)
# to make sure that it's usable in cpp11 mode.

# cython: language_level=3

from libcpp.condition_variable cimport *
from libcpp.mutex cimport mutex, timed_mutex, unique_lock, py_safe_construct_unique_lock
from libcpp cimport bool

from threading import Thread
import time

# define some placeholder chrono stuff for the sake of testing
cdef extern from "<chrono>" namespace "std::chrono" nogil:
    cdef cppclass milliseconds:
        milliseconds()
        milliseconds(long)

cdef extern from *:
    """
    namespace {
        std::chrono::time_point<std::chrono::steady_clock> get_time_point() {
            return std::chrono::time_point<std::chrono::steady_clock>::max();
        }

        using time_point_type = decltype(get_time_point());
    }
    """
    cdef cppclass time_point_type:
        pass

    time_point_type get_time_point()

cdef int global_value = 0

cdef bool global_value_predicate() noexcept nogil:
    return global_value > 0

ctypedef bool (*cfunc_predicate)() noexcept nogil

cpdef enum:
    NO_NOTIFY
    NOTIFY_ALL
    NOTIFY_ONE

cdef class CVHelperClass:
    cdef condition_variable cv
    cdef mutex m
    cdef const char* outcome

    def notify(self, int how_to_notify, new_value=None):
        global global_value

        if how_to_notify == NO_NOTIFY:
            return

        cdef bint new_value_is_none = new_value is None
        cdef int new_value_int = new_value if not new_value_is_none else -1
        with nogil:
            self.m.lock()
            try:
                if not new_value_is_none:
                    global_value = new_value_int
            finally:
                self.m.unlock()
            if how_to_notify == NOTIFY_ALL:
                self.cv.notify_all()
            elif how_to_notify == NOTIFY_ONE:
                self.cv.notify_one()

    cdef wait_on_new_thread(self, cfunc_predicate pred):
        with nogil:
            l = unique_lock[mutex](self.m)
        def thread_func():
            with nogil:
                l2 = unique_lock[mutex](self.m)
                if pred:
                    self.cv.wait(l2, pred)
                else:
                    self.cv.wait(l2)
        t = Thread(target=thread_func)
        t.start()
        return t

    cdef wait_for_on_new_thread(self, milliseconds duration, cfunc_predicate pred):
        with nogil:
            l = unique_lock[mutex](self.m)
        def thread_func():
            with nogil:
                l2 = unique_lock[mutex](self.m)
                if pred:
                    self.outcome = ("true" if self.cv.wait_for(l2, duration, pred) else "false")
                else:
                    self.outcome = ("timeout" if self.cv.wait_for(l2, duration) == cv_status.timeout else "no timeout")
        t = Thread(target=thread_func)
        t.start()
        return t


def test_cv_wait(bint use_predicate, int how_to_notify):
    """
    >>> test_cv_wait(False, NOTIFY_ALL)
    >>> test_cv_wait(False, NOTIFY_ONE)
    >>> test_cv_wait(True, NOTIFY_ALL)
    """
    global global_value
    global_value = 0
    helper = CVHelperClass()
    t = helper.wait_on_new_thread(global_value_predicate if use_predicate else <cfunc_predicate>NULL)
    if use_predicate:
        helper.notify(how_to_notify=how_to_notify, new_value=5)
        t.join()
    else:
        while t.is_alive():
            helper.notify(how_to_notify=how_to_notify, new_value=None)
            t.join(0.0)

def test_cv_wait_for(bint use_predicate, int how_to_notify, int ms):
    """
    >>> test_cv_wait_for(False, NO_NOTIFY, 1)
    b'timeout'
    >>> test_cv_wait_for(True, NO_NOTIFY, 1)
    b'false'
    >>> test_cv_wait_for(True, NOTIFY_ALL, 10000)
    b'true'
    >>> test_cv_wait_for(False, NOTIFY_ONE, 10000)
    b'no timeout'
    """
    global global_value
    global_value = 0
    helper = CVHelperClass()
    t = helper.wait_for_on_new_thread(milliseconds(ms), global_value_predicate if use_predicate else <cfunc_predicate>NULL)
    if use_predicate:
        helper.notify(how_to_notify=how_to_notify, new_value=5)
        t.join()
    else:
        while t.is_alive():
            helper.notify(how_to_notify=how_to_notify, new_value=None)
            t.join(0.0)
    return helper.outcome


# Use condition_variable_any and a different mutex type, but otherwise the tests
# are identical to the condition_variable ones
cdef class CVAnyHelperClass:
    cdef condition_variable_any cv
    cdef timed_mutex m
    cdef const char* outcome

    def notify(self, int how_to_notify, new_value=None):
        global global_value

        if how_to_notify == NO_NOTIFY:
            return

        cdef bint new_value_is_none = new_value is None
        cdef int new_value_int = new_value if not new_value_is_none else -1
        with nogil:
            self.m.lock()
            try:
                if not new_value_is_none:
                    global_value = new_value_int
            finally:
                self.m.unlock()
            if how_to_notify == NOTIFY_ALL:
                self.cv.notify_all()
            elif how_to_notify == NOTIFY_ONE:
                self.cv.notify_one()

    cdef wait_on_new_thread(self, cfunc_predicate pred):
        with nogil:
            l = unique_lock[timed_mutex](self.m)
        def thread_func():
            with nogil:
                l2 = unique_lock[timed_mutex](self.m)
                if pred:
                    self.cv.wait(l2, pred)
                else:
                    self.cv.wait(l2)
        t = Thread(target=thread_func)
        t.start()
        return t

    cdef wait_for_on_new_thread(self, milliseconds duration, cfunc_predicate pred):
        with nogil:
            l = unique_lock[timed_mutex](self.m)
        def thread_func():
            with nogil:
                l2 = unique_lock[timed_mutex](self.m)
                if pred:
                    self.outcome = ("true" if self.cv.wait_for(l2, duration, pred) else "false")
                else:
                    self.outcome = ("timeout" if self.cv.wait_for(l2, duration) == cv_status.timeout else "no timeout")
        t = Thread(target=thread_func)
        t.start()
        return t


def test_cv_any_wait(bint use_predicate, int how_to_notify):
    """
    >>> test_cv_any_wait(False, NOTIFY_ALL)
    >>> test_cv_any_wait(False, NOTIFY_ONE)
    >>> test_cv_any_wait(True, NOTIFY_ALL)
    """
    global global_value
    global_value = 0
    helper = CVAnyHelperClass()
    t = helper.wait_on_new_thread(global_value_predicate if use_predicate else <cfunc_predicate>NULL)
    if use_predicate:
        helper.notify(how_to_notify=how_to_notify, new_value=5)
        t.join()
    else:
        while t.is_alive():
            helper.notify(how_to_notify=how_to_notify, new_value=None)
            t.join(0.0)

def test_cv_any_wait_for(bint use_predicate, int how_to_notify, int ms):
    """
    >>> test_cv_any_wait_for(False, NO_NOTIFY, 1)
    b'timeout'
    >>> test_cv_any_wait_for(True, NO_NOTIFY, 1)
    b'false'
    >>> test_cv_any_wait_for(True, NOTIFY_ALL, 10000)
    b'true'
    >>> test_cv_any_wait_for(False, NOTIFY_ONE, 10000)
    b'no timeout'
    """
    global global_value
    global_value = 0
    helper = CVAnyHelperClass()
    t = helper.wait_for_on_new_thread(milliseconds(ms), global_value_predicate if use_predicate else <cfunc_predicate>NULL)
    if use_predicate:
        helper.notify(how_to_notify=how_to_notify, new_value=5)
        t.join()
    else:
        while t.is_alive():
            helper.notify(how_to_notify=how_to_notify, new_value=None)
            t.join(0.0)
    return helper.outcome

def test_py_safe_wait_basic(sleep_for):
    """
    >>> test_py_safe_wait_basic(None)
    >>> test_py_safe_wait_basic(0.05)
    >>> test_py_safe_wait_basic(0.0)
    """
    cdef condition_variable cv
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
    cdef condition_variable cv
    cdef mutex m
    success = False
    l = unique_lock[mutex](m)

    import sys

    def predicate():
        # The condition variable will always call this with the lock held
        return success

    def trigger():
        nonlocal success
        # needs the GIL (for the sake of testing)
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

def test_py_safe_wait_p(sleep_for):
    """
    >>> test_py_safe_wait_p(None)
    >>> test_py_safe_wait_p(0.05)
    >>> test_py_safe_wait_p(0.0)
    """
    global global_value
    global_value = 0

    cdef condition_variable cv
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

    # try wait_for (testing compilation, rather than timeout)
    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_for(cv, l, milliseconds(50000), global_value_predicate)
    t.join()

    # try wait_until (testing compilation, rather than timeout)
    global_value = 0
    t = Thread(target=trigger)
    t.start()
    py_safe_wait_until(cv, l, get_time_point(), global_value_predicate)
    t.join()
