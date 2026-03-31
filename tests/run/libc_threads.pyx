# mode: run
# tag: c11, no-cpp, no-macos

# cython: language_level=3

from libc cimport threads
from libc cimport time as ctime

from threading import Thread, Barrier
import time

def test_mutex():
    """
    test_mutex()
    """
    cdef threads.mtx_t m
    threads.mtx_init(&m, threads.mtx_plain)
    threads.mtx_lock(&m)
    threads.mtx_unlock(&m)
    threads.mtx_destroy(&m)

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

def test_py_safe_lock(n_threads):
    """
    >>> test_py_safe_lock(4)
    2000
    """
    cdef threads.mtx_t m
    threads.mtx_init(&m, threads.mtx_plain)

    barrier = Barrier(n_threads)
    cdef int count = 0

    def thread_func():
        nonlocal count

        barrier.wait()
        for i in range(500):
            if i%2:
                with nogil:
                    threads.py_safe_mtx_lock(&m)
                    try:
                        count += 1
                    finally:
                        threads.mtx_unlock(&m)
            else:
                threads.py_safe_mtx_lock(&m)
                try:
                    count += 1
                finally:
                    threads.mtx_unlock(&m)

    all_threads = [
        Thread(target=thread_func) for _ in range(n_threads)
    ]
    for t in all_threads:
        t.start()
    for t in all_threads:
        t.join()
    print(count)
    threads.mtx_destroy(&m)

def test_py_safe_lock_nogil():
    """
    >>> test_py_safe_lock_nogil()
    """
    cdef threads.mtx_t m
    threads.mtx_init(&m, threads.mtx_plain)

    with nogil:
        threads.py_safe_mtx_lock(&m)
        threads.mtx_unlock(&m)

    threads.mtx_destroy(&m)

def test_py_safe_cnd_wait():
    """
    >>> test_py_safe_cnd_wait()
    10 True
    """
    cdef threads.cnd_t condition_var
    threads.cnd_init(&condition_var)
    cdef threads.mtx_t m
    threads.mtx_init(&m, threads.mtx_plain)

    cdef object value = 0
    cdef object done = False

    def wait_on_condition_var():
        nonlocal done

        threads.py_safe_mtx_lock(&m)
        try:
            wait_result = threads.thrd_success
            while wait_result == threads.thrd_success and value <= 5:
                threads.py_safe_cnd_wait(&condition_var, &m)
            if value > 5:
                done = True
        finally:
            threads.mtx_unlock(&m)

    t1 = Thread(target=wait_on_condition_var)
    t1.start()

    def set_value():
        nonlocal value
        for i in range(10):
            threads.py_safe_mtx_lock(&m)
            try:
                value += 1
            finally:
                threads.mtx_unlock(&m)
            threads.cnd_signal(&condition_var)

    t2 = Thread(target=set_value)
    t2.start()

    t1.join()
    t2.join()
    threads.mtx_destroy(&m)
    threads.cnd_destroy(&condition_var)

    print(value, done)

def test_py_safe_cnd_timed_wait(fail):
    """
    >>> test_py_safe_cnd_timed_wait(False)
    True
    >>> test_py_safe_cnd_timed_wait(True)
    False
    """
    cdef threads.cnd_t condition_var
    threads.cnd_init(&condition_var)
    cdef threads.mtx_t m
    threads.mtx_init(&m, threads.mtx_plain)

    condition = False
    condition_var_succeeded = False

    def wait_on_condition_var():
        nonlocal condition_var_succeeded

        cdef ctime.timespec ts
        ctime.timespec_get(&ts, ctime.TIME_UTC);
        if fail:
            # don't wait too long to not do anything
            ts.tv_nsec += 100_000_000  # 100 ms
            if ts.tv_nsec > 1000_000_000:  # 1s
                ts.tv_nsec -= 1000_000_000
                ts.tv_sec += 1
        else:
            ts.tv_sec += 10  # make the test robust

        threads.py_safe_mtx_lock(&m)
        try:
            result = threads.thrd_success
            while result == threads.thrd_success and not condition:
                result = threads.py_safe_cnd_timedwait(
                    &condition_var, &m, &ts
                )
            if condition:
                condition_var_succeeded = True
                return
        finally:
            threads.mtx_unlock(&m)

    t = Thread(target=wait_on_condition_var)
    t.start()
    threads.py_safe_mtx_lock(&m)
    try:
        if not fail:
            condition = True
            threads.cnd_broadcast(&condition_var)
    finally:
        threads.mtx_unlock(&m);

    t.join()
    print(condition_var_succeeded)
    threads.mtx_destroy(&m)
    threads.cnd_destroy(&condition_var)
