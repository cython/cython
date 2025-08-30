# mode: run
# tag: cpp, cpp11

from libcpp cimport future
from libcpp.exception cimport make_exception_ptr

cdef extern from "<stdexcept>" namespace "std" nogil:
    cdef cppclass runtime_error:
        runtime_error(const char*)

cdef extern from "<chrono>" namespace "std::chrono" nogil:
    cdef cppclass milliseconds:
        milliseconds(int v)

def test_basic_usage():
    """
    >>> test_basic_usage()
    """
    cdef future.promise[int] p = future.promise[int]()
    f = p.get_future()
    assert f.valid()

    p.set_value(5)
    f.wait()  # shouldn't actually do anything
    assert f.get() == 5

def test_basic_usage_void():
    """
    >>> test_basic_usage_void()
    """
    cdef future.promise[void] p = future.promise[void]()
    f = p.get_future()
    assert f.valid()

    p.set_value()
    f.wait()  # shouldn't actually do anything
    f.get()

def test_set_exception(msg):
    """
    >>> test_set_exception(b"error message")
    Traceback (most recent call last):
    ...
    RuntimeError: error message
    """
    cdef future.promise[int] p = future.promise[int]()
    f = p.get_future()

    p.set_exception(make_exception_ptr(runtime_error(msg)))
    f.get()


def test_shared():
    """
    >>> test_shared()
    """
    cdef future.promise[int] p = future.promise[int]()
    f = p.get_future().share()

    p.set_value(5)
    assert f.get() == 5

def test_shared_void():
    """
    >>> test_shared()
    """
    cdef future.promise[void] p = future.promise[void]()
    f = p.get_future().share()

    p.set_value()
    f.get()


def test_custom_error_handling():
    """
    >>> test_custom_error_handling()
    std::future_error
    True
    """
    cdef future.promise[void] p = future.promise[void]()

    p.set_value()
    try:
        p.set_value()
    except RuntimeError as e:
        print(e.args[0])
        print(e.args[1] == future.future_errc.promise_already_satisfied)

def test_timeout():
    """
    >>> test_timeout()
    """
    cdef future.promise[void] p = future.promise[void]()
    f = p.get_future()

    assert f.wait_for(milliseconds(1)) == future.future_status.timeout
    p.set_value()
    assert f.wait_for(milliseconds(1)) == future.future_status.ready
