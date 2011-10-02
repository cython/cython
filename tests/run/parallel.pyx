# tag: run
# tag: openmp

cimport cython.parallel
from cython.parallel import prange, threadid
cimport openmp
from libc.stdlib cimport malloc, free

openmp.omp_set_nested(1)

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

cdef int get_num_threads() with gil:
    print "get_num_threads called"
    return 3

def test_num_threads():
    """
    >>> test_num_threads()
    1
    get_num_threads called
    3
    get_num_threads called
    3
    """
    cdef int dyn = openmp.omp_get_dynamic()
    cdef int num_threads
    cdef int *p = &num_threads

    openmp.omp_set_dynamic(0)

    with nogil, cython.parallel.parallel(num_threads=1):
        p[0] = openmp.omp_get_num_threads()

    print num_threads

    with nogil, cython.parallel.parallel(num_threads=get_num_threads()):
        p[0] = openmp.omp_get_num_threads()

    print num_threads

    cdef int i
    num_threads = 0xbad
    for i in prange(1, nogil=True, num_threads=get_num_threads()):
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


OPENMP_PARALLEL = True
include "sequential_parallel.pyx"
