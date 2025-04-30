# mode: run
# tag: cpp, cpp20, no-cpp-locals

from libcpp cimport stop_token
import threading

def test_basic_usage1():
    """
    >>> test_basic_usage1()
    """
    ss = stop_token.stop_source()
    assert not ss.stop_requested()
    assert ss.stop_possible()

    st = ss.get_token()
    assert not st.stop_requested()
    assert st.stop_possible()

    ss.request_stop()
    assert st.stop_requested()
    assert ss.stop_requested()

def test_basic_usage2():
    """
    >>> test_basic_usage2()
    """
    ss = stop_token.stop_source(stop_token.nostopstate)
    assert not ss.stop_requested()
    assert not ss.stop_possible()
    
    ss.request_stop()
    assert not ss.stop_requested()

cdef int global_flag = 0

cdef void use_as_stop_callback() nogil noexcept:
    global_flag = 1

def test_cfunc_stop_callback():
    """
    >>> test_cfunc_stop_callback()
    """
    global global_flag

    global_flag = 1

    ss = stop_token.stop_source()
    
    def other_thread():
        ss.request_stop()

    # stop callback is hard to use except on the heap because it can't be
    # default constructed or assigned
    cb = new stop_token.func_ptr_stop_callback(ss.get_token(), use_as_stop_callback)
    try:
        t = threading.Thread(target=other_thread)
        t.start()
        t.join()

        assert global_flag
    finally:
        del cb

def test_python_stop_callback_wrapper():
    """
    >>> test_python_stop_callback_wrapper()
    """
    cdef stop_token.python_stop_callback_holder cb_holder
    ss = stop_token.stop_source()

    local_flag = False

    def callback_func():
        nonlocal local_flag
        local_flag = True

    cb_holder.initialize(ss.get_token(), callback_func)

    def other_thread():
        ss.request_stop()

    t = threading.Thread(target=other_thread)
    t.start()
    t.join()

    assert local_flag
