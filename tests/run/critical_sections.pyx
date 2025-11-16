# mode: run

cimport cython

import threading

# This test is most useful on free-threading builds.
# It should pass on regular builds just by virtue of
# the GIL.

def _create_identical_threads(n_threads, target):
    return [
        threading.Thread(target=target)
        for _ in range(n_threads)
    ]

def _run_threads_to_completion(threads):
    for t in threads:
        t.start()
    for t in threads:
        t.join()

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

    threads = _create_identical_threads(n_threads, worker)
    _run_threads_to_completion(threads)

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
    _run_threads_to_completion(threads)

    # Each variable is modified from 2 threads
    expected = ((n_loops * (n_loops - 1))/2)*2
    assert a == expected, (a, expected)
    assert b == expected, (b, expected)


cdef class CClass:
    cdef int count
    def __cinit__(self):
        self.count = 0

    @cython.critical_section
    def increment(self, other):
        self.count += other

    @cython.critical_section
    def increment_one(self):
        self.count += 1

    @cython.critical_section
    cpdef increment_one_cp(self):
        self.count += 1

    @cython.critical_section
    cdef increment_one_c(self):
        self.count += 1


def test_class_critical_section_decorator(n_threads, n_loops):
    """
    >>> test_class_critical_section_decorator(4, 100)
    """
    barrier = threading.Barrier(n_threads)

    instance = CClass()

    def worker():
        nonlocal instance
        barrier.wait()
        for i in range(n_loops):
            remainder = i % 4
            if remainder == 0:
                instance.increment_one()
            elif remainder == 1:
                instance.increment(1)
            elif remainder == 2:
                instance.increment_one_c()
            else:
                instance.increment_one_cp()

    threads = _create_identical_threads(n_threads, worker)
    _run_threads_to_completion(threads)

    expected = n_loops*n_threads
    assert instance.count == expected, (instance.count, expected)


def test_free_function_with_critical_section(n_threads, n_loops):
    """
    >>> test_free_function_with_critical_section(4, 100)
    """
    cdef int count = 0
    lock = object()
    barrier = threading.Barrier(n_threads)

    @cython.test_assert_path_exists("//CriticalSectionStatNode")
    @cython.critical_section
    def inner(lock):
        @cython.test_fail_if_path_exists("//CriticalSectionStatNode")
        def inner_inner():
            pass  # Unused - just to test the directive one-level only


        nonlocal count
        count += 1

    def worker():
        barrier.wait()
        for i in range(n_loops):
            inner(lock)

    threads = _create_identical_threads(n_threads, worker)
    _run_threads_to_completion(threads)

    expected = n_loops*n_threads
    assert count == expected, (count, expected)

def test_critical_section_mutex(n_threads, n_loops):
    """
    >>> test_critical_section_mutex(4, 100)
    """
    cdef int count = 0
    cdef cython.pymutex lock
    barrier = threading.Barrier(n_threads)

    def worker():
        nonlocal count
        barrier.wait()
        for i in range(n_loops):
            with cython.critical_section(lock):
                count += i

    threads = _create_identical_threads(n_threads, worker)
    _run_threads_to_completion(threads)

    expected = ((n_loops * (n_loops - 1))/2)*n_threads
    assert count == expected, (count, expected)

def test_critical_section_p_mutex(n_threads, n_loops):
    """
    >>> test_critical_section_p_mutex(4, 100)
    """
    cdef int count = 0
    cdef cython.pymutex lock
    barrier = threading.Barrier(n_threads)

    def worker():
        nonlocal count
        barrier.wait()
        for i in range(n_loops):
            with cython.critical_section(&lock):
                count += i

    threads = _create_identical_threads(n_threads, worker)
    _run_threads_to_completion(threads)

    expected = ((n_loops * (n_loops - 1))/2)*n_threads
    assert count == expected, (count, expected)

def test_critical_section_mutexes(n_loops):
    """
    >>> test_critical_section_mutexes(100)
    """
    cdef int a = 0
    cdef int b = 0
    barrier = threading.Barrier(3)
    cdef cython.pymutex lock_a
    cdef cython.pymutex lock_b

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
            with cython.critical_section(&lock_a, lock_b):
                a += i
                b += i

    threads = [
        threading.Thread(target=target)
        for target in [a_thread, b_thread, ab_thread]
    ]
    _run_threads_to_completion(threads)

    # Each variable is modified from 2 threads
    expected = ((n_loops * (n_loops - 1))/2)*2
    assert a == expected, (a, expected)
    assert b == expected, (b, expected)
