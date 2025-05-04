# mode: run
# tag: c11, no-cpp, no-macos

# cython: language_level=3

from libc cimport threads

def test_mutex():
    """
    test_mutex()
    """
    cdef threads.mtx_t m
    threads.mtx_init(&m, threads.mtx_plain)
    threads.mtx_lock(&m)
    threads.mtx_unlock(&m)

cdef void call_me_once() noexcept with gil:
    # with gil is only OK because it's a toy example with no other threads so no chance of deadlock.
    # Do not copy this code!
    print("Listen very carefully, I shall say this only once.")

def test_once():
    """
    >>> test_once()
    Listen very carefully, I shall say this only once.
    """
    cdef threads.once_flag flag
    threads.once_flag_init(&flag)
    threads.call_once(&flag, &call_me_once)
    threads.call_once(&flag, &call_me_once)

cdef int my_thread_func(void* arg) noexcept nogil:
    cdef int x = (<int*>arg)[0]
    t = threads.thrd_current()  # compile test - nothing useful to do with it
    return x

def test_thread():
    """
    >>> test_thread()
    """
    cdef threads.thrd_t t
    cdef int one = 1
    threads.thrd_create(&t, my_thread_func, &one)
    cdef int result = 0
    threads.thrd_join(t, &result)
    assert result==1, result
