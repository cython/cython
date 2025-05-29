# tag: run
# tag: openmp

from cython.parallel import prange, parallel, threadid
cimport openmp

# A very simple test function to call while holding the gil.
def f(x):
    return x

def test_parallel_with_python():
    """
    >>> test_parallel_with_python()
    """
    cdef int maxthreads = openmp.omp_get_max_threads()
    lst = [None]*maxthreads

    with parallel(with_python=True):
        # Writing into a list should be thread-safe in Cython, especially
        # since they're all writing different elements
        lst[threadid()] = threadid()

    for i in range(maxthreads):
        assert lst[i] == i

def test_parallel_nogil_with_python():
    """
    >>> test_parallel_nogil_with_python()
    """
    cdef int maxthreads = openmp.omp_get_max_threads()
    lst = [None]*maxthreads

    with nogil:
        with parallel(with_python=True):
            # Writing into a list should be thread-safe in Cython, especially
            # since they're all writing different elements
            lst[threadid()] = threadid()

    for i in range(maxthreads):
        assert lst[i] == i

cdef void test_parallel_maybe_nogil_with_python_impl() nogil:
    cdef int maxthreads = openmp.omp_get_max_threads()
    with gil:
        lst = [None]*maxthreads

    with parallel(with_python=True):
        # Writing into a list should be thread-safe in Cython, especially
        # since they're all writing different elements
        lst[threadid()] = threadid()

    with gil:
        for i in range(maxthreads):
            assert lst[i] == i

def test_parallel_maybe_nogil_with_python(release_gil):
    """
    >>> test_parallel_maybe_nogil_with_python(True)
    >>> test_parallel_maybe_nogil_with_python(False)
    """
    if release_gil:
        with nogil:
            test_parallel_maybe_nogil_with_python_impl()
    else:
        test_parallel_maybe_nogil_with_python_impl()


def test_prange_with_python():
    """
    >>> test_prange_with_python()
    """

    cdef int i = 0;

    out = [None]*100

    for i in prange(100, with_python=True):
        out[i] = f(i)

    for i in range(100):
        assert out[i] == i

def test_prange_nogil_with_python():
    """
    >>> test_prange_nogil_with_python()
    """
    cdef int i = 0;

    out = [None]*100

    with nogil:
        for i in prange(100, with_python=True):
            out[i] = f(i)

    for i in range(100):
        assert out[i] == i

cdef void test_prange_maybe_nogil_with_python_impl() nogil:
    cdef int i = 0;

    with gil:
        out = [None]*100

    for i in prange(100, with_python=True):
        out[i] = f(i)

    with gil:
        for i in range(100):
            assert out[i] == i

def test_prange_maybe_nogil_with_python(release_gil):
    """
    >>> test_prange_maybe_nogil_with_python(True)
    >>> test_prange_maybe_nogil_with_python(False)
    """
    if release_gil:
        with nogil:
            test_prange_maybe_nogil_with_python_impl()
    else:
        test_prange_maybe_nogil_with_python_impl()

def test_parallel_prange_with_python():
    """
    >>> test_parallel_prange_with_python()
    """
    cdef int i = 0;

    out = [None]*100

    with parallel(with_python=True):
        for i in prange(100, with_python=True):
            out[i] = f(i)

    for i in range(100):
        assert out[i] == i
