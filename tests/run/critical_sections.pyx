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
    cdef int a = 2
    cdef int b = 3
    barrier = threading.Barrier(3)
    finished_event = threading.Event()
    failed = threading.Event()
    lock_a = object()
    lock_b = object()

    def reader1():
        barrier.wait()
        while not finished_event.is_set():
            for _ in range(10):
                with cython.critical_section(lock_a):
                    if not (a==2 or a==3):
                        failed.set()

    def reader2():
        barrier.wait()
        while not finished_event.is_set():
            for _ in range(10):
                with cython.critical_section(lock_b):
                    if not (b==2 or b==3):
                        failed.set()

    def swapper():
        nonlocal a, b
        barrier.wait()
        for _ in range(n_loops):
            with cython.critical_section(lock_a, lock_b):
                old_a = a
                old_b = b
                a = 1000
                b = 2000
                a = old_b
                b = old_a
        finished_event.set()
    t1 = threading.Thread(target=reader1)
    t2 = threading.Thread(target=reader2)
    t3 = threading.Thread(target=swapper)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

    assert not failed.is_set()

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
