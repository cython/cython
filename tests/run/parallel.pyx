# tag: run
# distutils: libraries = gomp
# distutils: extra_compile_args = -fopenmp

cimport cython.parallel
from cython.parallel import prange, threadid
cimport openmp
from libc.stdlib cimport malloc, free
from libc.stdio cimport puts

import sys

try:
    from builtins import next # Py3k
except ImportError:
    def next(it):
        return it.next()

#@cython.test_assert_path_exists(
#    "//ParallelWithBlockNode//ParallelRangeNode[@schedule = 'dynamic']",
#    "//GILStatNode[@state = 'nogil]//ParallelRangeNode")
def test_prange():
    """
    >>> test_prange()
    (9, 9, 45, 45)
    """
    cdef Py_ssize_t i, j, sum1 = 0, sum2 = 0

    with nogil, cython.parallel.parallel:
        for i in prange(10, schedule='dynamic'):
            sum1 += i

    for j in prange(10, nogil=True):
        sum2 += j

    return i, j, sum1, sum2

def test_descending_prange():
    """
    >>> test_descending_prange()
    5
    """
    cdef int i, start = 5, stop = -5, step = -2
    cdef int sum = 0

    for i in prange(start, stop, step, nogil=True):
        sum += i

    return sum

def test_propagation():
    """
    >>> test_propagation()
    (9, 9, 9, 9, 450, 450)
    """
    cdef int i, j, x, y
    cdef int sum1 = 0, sum2 = 0

    for i in prange(10, nogil=True):
        for j in prange(10):
            sum1 += i

    with nogil, cython.parallel.parallel:
        for x in prange(10):
            with cython.parallel.parallel:
                for y in prange(10):
                    sum2 += y

    return i, j, x, y, sum1, sum2


def test_parallel():
    """
    >>> test_parallel()
    """
    cdef int maxthreads = openmp.omp_get_max_threads()
    cdef int *buf = <int *> malloc(sizeof(int) * maxthreads)

    if buf == NULL:
        raise MemoryError

    with nogil, cython.parallel.parallel:
        buf[threadid()] = threadid()

    for i in range(maxthreads):
        assert buf[i] == i

    free(buf)

def test_unsigned_operands():
    """
    This test is disabled, as this currently does not work (neither does it
    for 'for i from x < i < y:'. I'm not sure we should strife to support
    this, at least the C compiler gives a warning.

    test_unsigned_operands()
    10
    """
    cdef int i
    cdef int start = -5
    cdef unsigned int stop = 5
    cdef int step = 1

    cdef int steps_taken = 0

    for i in prange(start, stop, step, nogil=True):
        steps_taken += 1

    return steps_taken

def test_reassign_start_stop_step():
    """
    >>> test_reassign_start_stop_step()
    20
    """
    cdef int start = 0, stop = 10, step = 2
    cdef int i
    cdef int sum = 0

    for i in prange(start, stop, step, nogil=True):
        start = -2
        stop = 2
        step = 0

        sum += i

    return sum

def test_closure_parallel_privates():
    """
    >>> test_closure_parallel_privates()
    9 9
    45 45
    0 0 9 9
    """
    cdef int x

    def test_target():
        nonlocal x
        for x in prange(10, nogil=True):
            pass
        return x

    print test_target(), x

    def test_reduction():
        nonlocal x
        cdef int i

        x = 0
        for i in prange(10, nogil=True):
            x += i

        return x

    print test_reduction(), x

    def test_generator():
        nonlocal x
        cdef int i

        x = 0
        yield x
        x = 2

        for i in prange(10, nogil=True):
            x = i

        yield x

    g = test_generator()
    print next(g), x, next(g), x

def test_pure_mode():
    """
    >>> test_pure_mode()
    0
    1
    2
    3
    4
    4
    3
    2
    1
    0
    0
    """
    import Cython.Shadow
    pure_parallel = sys.modules['cython.parallel']

    for i in pure_parallel.prange(5):
        print i

    for i in pure_parallel.prange(4, -1, -1, schedule='dynamic', nogil=True):
        print i

    with pure_parallel.parallel:
        print pure_parallel.threadid()

