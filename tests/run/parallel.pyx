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

#include "sequential_parallel.pyx"
