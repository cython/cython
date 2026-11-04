# tag: run
# tag: openmp, threads

# cython: test_assert_c_code_has = omp for (?:first)?private\(__pyx_v_first_loop_target\)
# cython: test_assert_c_code_has = omp for nowait (?:first)?private\(__pyx_v_last_loop_target\)

cimport cython.parallel
from cython.parallel import prange, threadid
cimport openmp
from libc.stdlib cimport malloc, calloc, free

openmp.omp_set_nested(1)

cdef int forward(int x) nogil:
    return x

def test_parallel():
    """
    >>> test_parallel()
    """
    cdef int maxthreads = openmp.omp_get_max_threads()
    cdef int *buf = <int *> malloc(sizeof(int) * maxthreads)

    if buf == NULL:
        raise MemoryError

    with nogil, cython.parallel.parallel():
        buf[threadid()] = threadid()
        # Recognise threadid() also when it's used in a function argument.
        # See https://github.com/cython/cython/issues/3594
        buf[forward(cython.parallel.threadid())] = forward(threadid())

    for i in range(maxthreads):
        assert buf[i] == i

    free(buf)

cdef int get_num_threads() noexcept with gil:
    print "get_num_threads called"
    return 3

cdef bint check_size(int size) nogil:
    return size > 5

def test_num_threads(int size):
    """
    >>> test_num_threads(6)
    1
    get_num_threads called
    3
    get_num_threads called
    3
    get_num_threads called
    3
    get_num_threads called
    3
    >>> test_num_threads(4)
    1
    get_num_threads called
    1
    get_num_threads called
    1
    get_num_threads called
    1
    get_num_threads called
    1
    """
    cdef int dyn = openmp.omp_get_dynamic()
    cdef int num_threads
    cdef int *p = &num_threads

    openmp.omp_set_dynamic(0)

    with nogil, cython.parallel.parallel(num_threads=1):
        p[0] = openmp.omp_get_num_threads()

    print num_threads

    with nogil, cython.parallel.parallel(num_threads=get_num_threads(), use_threads_if=size > 5):
        p[0] = openmp.omp_get_num_threads()

    print num_threads

    # Checks that temporary variables are released properly
    with nogil, cython.parallel.parallel(num_threads=get_num_threads(), use_threads_if=check_size(size)):
        p[0] = openmp.omp_get_num_threads()

    print num_threads

    cdef int i
    # Checks that temporary variables are released properly
    for i in prange(1, nogil=True, num_threads=get_num_threads(), use_threads_if=check_size(size)):
        p[0] = openmp.omp_get_num_threads()
        break

    print num_threads

    num_threads = 0xbad
    for i in prange(1, nogil=True, num_threads=get_num_threads(), use_threads_if=size > 5):
        p[0] = openmp.omp_get_num_threads()
        break

    openmp.omp_set_dynamic(dyn)

    return num_threads

cdef int parallel_0_threads() noexcept:
    # num_threads == 0 is interpreted as "default" and so should compile and run
    with nogil, cython.parallel.parallel(num_threads=0):
        return openmp.omp_get_num_threads()

def test_0_threads():
    """
    >>> test_0_threads()
    True
    """
    return parallel_0_threads() > 0

cdef int parallel_0_threads_dynamic(int num_threads) noexcept:
    with nogil, cython.parallel.parallel(num_threads=num_threads):
        return openmp.omp_get_num_threads()

def test_0_threads_dynamic(num_threads):
    """
    0 threads passed as a runtime argument also works to make openp use
    the default.

    >>> test_0_threads_dynamic(0)
    True
    >>> test_0_threads_dynamic(5)
    True
    """
    return parallel_0_threads_dynamic(num_threads) > 0

cdef int prange_0_threads() noexcept:
    # num_threads == 0 is interpreted as "default" and so should compile and run
    cdef int arr[10]
    for i in prange(10, nogil=True, num_threads=0):
        arr[i] = openmp.omp_get_num_threads()
    return arr[0]

def test_prange_0_threads():
    """
    >>> test_prange_0_threads()
    True
    """
    count = prange_0_threads()
    assert count > 0, count
    return count > 0

cdef int prange_0_threads_dynamic(int num_threads) noexcept:
    # a runtime value of num_threads == 0 can be used to select the default number of threads
    # so should compile and run.
    cdef int arr[10]
    for i in prange(10, nogil=True, num_threads=num_threads):
        arr[i] = openmp.omp_get_num_threads()
    return arr[0]

def test_prange_0_threads_dynamic(num_threads):
    """
    >>> test_prange_0_threads_dynamic(0)
    True
    >>> test_prange_0_threads_dynamic(10)
    True
    """
    count = prange_0_threads_dynamic(num_threads)
    assert count > 0, count
    return count > 0


'''
def test_parallel_catch():
    """
    >>> test_parallel_catch()
    True
    """
    cdef int i, j, num_threads
    exceptions = []

    for i in prange(100, nogil=True, num_threads=4):
        num_threads = openmp.omp_get_num_threads()

        with gil:
            try:
                for j in prange(100, nogil=True):
                    if i + j > 60:
                        with gil:
                            raise Exception("try and catch me if you can!")
            except Exception as e:
                exceptions.append(e)
                break

    print len(exceptions) == num_threads
    assert len(exceptions) == num_threads, (len(exceptions), num_threads)
'''


cdef void parallel_exception_checked_function(int* ptr, int id) except * nogil:
    # requires the GIL after each call
    ptr[0] = id;

cdef void parallel_call_exception_checked_function_impl(int* arr, int num_threads) nogil:
    # Inside a nogil function, parallel can't be sure that the GIL has been released.
    # Therefore Cython must release the GIL itself.
    # Otherwise, we can experience cause lock-ups if anything inside it acquires the GIL
    # (since if any other thread has finished, it will be holding the GIL).
    #
    # An equivalent test with prange is in "sequential_parallel.pyx"
    with cython.parallel.parallel(num_threads=num_threads):
        parallel_exception_checked_function(arr+threadid(), threadid())


def test_parallel_call_exception_checked_function():
    """
    test_parallel_call_exception_checked_function()
    """
    cdef int maxthreads = openmp.omp_get_max_threads()
    cdef int *buf = <int *> malloc(sizeof(int) * maxthreads)

    if buf == NULL:
        raise MemoryError

    try:
        # Note we *don't* release the GIL here
        parallel_call_exception_checked_function_impl(buf, maxthreads)

        for i in range(maxthreads):
            assert buf[i] == i
    finally:
        free(buf)


def test_prange_barrier_between_loops():
    """
    Only the loop followed by code in the block keeps its end barrier.

    >>> test_prange_barrier_between_loops()
    0
    """
    cdef int first_loop_target, last_loop_target, n_stale = 0
    cdef int a[100]
    for first_loop_target in range(100):
        a[first_loop_target] = 0
    with nogil, cython.parallel.parallel(num_threads=4):
        for first_loop_target in prange(100, schedule='static'):
            a[first_loop_target] = 1
        for last_loop_target in prange(100, schedule='static'):
            if a[99 - last_loop_target] == 0:
                n_stale += 1
    return n_stale


OPENMP_PARALLEL = True
include "sequential_parallel.pyx"


def test_prange_end_barrier(int n=400, int nthreads=4):
    """
    Code after a prange in a parallel block must see all of its iterations.

    >>> test_prange_end_barrier()
    0
    """
    import time
    cdef int i, k, late = n - n // nthreads, n_stale = 0
    cdef int *n_stale_ptr = &n_stale
    cdef int *a = <int *> calloc(n, sizeof(int))

    with nogil, cython.parallel.parallel(num_threads=nthreads):
        for i in prange(n, schedule='static'):
            if i == late:
                with gil:
                    time.sleep(0.02)
            a[i] = 1
        for k in range(n):
            if a[k] == 0:
                with gil:
                    n_stale_ptr[0] += 1
                break

    free(a)
    return n_stale
