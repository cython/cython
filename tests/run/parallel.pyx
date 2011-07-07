# tag: run
# tag: openmp

cimport cython.parallel
from cython.parallel import prange, threadid
cimport openmp
from libc.stdlib cimport malloc, free

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

    for i in range(maxthreads):
        assert buf[i] == i

    free(buf)

def test_num_threads():
    """
    >>> test_num_threads()
    1
    """
    cdef int dyn = openmp.omp_get_dynamic()
    cdef int num_threads
    cdef int *p = &num_threads

    openmp.omp_set_dynamic(0)

    with nogil, cython.parallel.parallel(num_threads=1):
        p[0] = openmp.omp_get_num_threads()

    openmp.omp_set_dynamic(dyn)

    return num_threads

OPENMP_PARALLEL = True
include "sequential_parallel.pyx"
