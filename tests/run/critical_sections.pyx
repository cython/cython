# mode: run

cimport cython

import threading

# This test is most useful on free-threading builds.
# It should pass on regular builds just by virtue of
# the GIL.

def test_single_critical_section(n_threads, n_loops):
    """
    >>> test_single_critical_section(4, 100)
    """
    cdef int count = 0
    lock = object()
    barrier = threading.Barrier(n_threads)

    def worker():
        nonlocal count
        barrier.wait()
        for i in range(n_loops):
            with cython.critical_section(lock):
                count += i

    threads = [
        threading.Thread(target=worker)
        for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = ((n_loops * (n_loops - 1))/2)*n_threads
    assert count == expected, (count, expected)


def test_double_critical_section(n_loops):
    """
    >>> test_double_critical_section(100)
    """
    cdef int a = 0
    cdef int b = 0
    barrier = threading.Barrier(3)
    lock_a = object()
    lock_b = object()

    def a_thread():
        nonlocal a
        barrier.wait()
        for i in range(n_loops):
            with cython.critical_section(lock_a):
                a += i

    def b_thread():
        nonlocal b
        barrier.wait()
        for i in range(n_loops):
            with cython.critical_section(lock_b):
                b += i

    def ab_thread():
        nonlocal a, b
        barrier.wait()
        for i in range(n_loops):
            with cython.critical_section(lock_a, lock_b):
                a += i
                b += i

    threads = [
        threading.Thread(target=target)
        for target in [a_thread, b_thread, ab_thread]
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Each variable is modified from 2 threads
    expected = ((n_loops * (n_loops - 1))/2)*2
    assert a == expected, (a, expected)
    assert b == expected, (b, expected)


def test_critical_section_in_generators(n_threads, n_loops):
    """
    >>> test_critical_section_in_generators(4, 100)
    """
    cdef int count = 0
    lock = object()
    barrier = threading.Barrier(n_threads)

    def gen():
        nonlocal count
        barrier.wait()
        with cython.critical_section(lock):
            for i in range(n_loops):
                count += i
                yield

    def make_and_run_generator():
        g = gen()
        for _ in g:
            pass

    threads = [
        threading.Thread(target=make_and_run_generator)
        for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = ((n_loops * (n_loops - 1))/2)*n_threads
    assert count == expected, (count, expected)
