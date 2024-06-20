# tag: run
# tag: openmp

cimport cython.parallel
from cython.parallel import prange, threadid
cimport openmp
from libc.stdlib cimport malloc, free

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
            except Exception, e:
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


OPENMP_PARALLEL = True
include "sequential_parallel.pyx"
