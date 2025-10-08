# tag: run
# tag: openmp, warnings

# Without freethreading_compatible this test will generate warnings to let us know
# that parallel+GIL won't work well.
# cython: freethreading_compatible=True

from cython.parallel import prange, parallel, threadid
cimport cython
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

    with parallel():
        # Writing into a list should be thread-safe in Cython, especially
        # since they're all writing different elements
        lst[threadid()] = threadid()

    for i in range(maxthreads):
        assert lst[i] == i

@cython.test_assert_path_exists("//GILStatNode[@state='nogil']//ParallelWithBlockNode[@acquire_gil=True]")
@cython.test_fail_if_path_exists("//GILStatNode//GILStatNode")
def test_parallel_nogil_with_python():
    """
    >>> test_parallel_nogil_with_python()
    """
    cdef int maxthreads = openmp.omp_get_max_threads()
    lst = [None]*maxthreads

    with nogil:
        # although this is how we want users to write it, we should transform it internally
        # to minimize gil juggling
        with gil:
            with parallel():
                # Writing into a list should be thread-safe in Cython, especially
                # since they're all writing different elements
                lst[threadid()] = threadid()

    for i in range(maxthreads):
        assert lst[i] == i

@cython.test_assert_path_exists("//GILStatNode[@state='nogil']//ParallelWithBlockNode[@acquire_gil=True]")
@cython.test_fail_if_path_exists("//GILStatNode//GILStatNode")
cdef void test_parallel_maybe_nogil_with_python_impl() nogil:
    cdef int maxthreads = openmp.omp_get_max_threads()
    with gil:
        lst = [None]*maxthreads

    # Although this is how we want users to write it, we should transform it to minimize
    # juggling the GIL.
    with gil:
        with parallel():
            # Writing into a list should be thread-safe in Cython, especially
            # since they're all writing different elements
            lst[threadid()] = threadid()

    # separate - for testing rather than part of the transform
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

    cdef int i = 0

    out = [None]*100

    for i in prange(100):
        out[i] = f(i)

    for i in range(100):
        assert out[i] == i

@cython.test_assert_path_exists("//GILStatNode[@state='nogil']//ParallelRangeNode[@acquire_gil=True]")
@cython.test_fail_if_path_exists("//GILStatNode//GILStatNode")
def test_prange_nogil_with_python():
    """
    >>> test_prange_nogil_with_python()
    """
    cdef int i = 0

    out = [None]*100

    with nogil:
        # Although this is how we want users to write it, we should still
        # transform it internally to minimize GIL juggling.
        with gil:
            for i in prange(100):
                out[i] = f(i)

    for i in range(100):
        assert out[i] == i

@cython.test_assert_path_exists("//GILStatNode[@state='nogil']//ParallelRangeNode[@acquire_gil=True]")
@cython.test_fail_if_path_exists("//GILStatNode//GILStatNode")
cdef void test_prange_maybe_nogil_with_python_impl() nogil:
    cdef int i = 0

    with gil:
        out = [None]*100

    with gil:
        for i in prange(100):
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
    cdef int i = 0

    out = [None]*100

    with parallel():
        for i in prange(100):
            out[i] = f(i)

    for i in range(100):
        assert out[i] == i

_WARNINGS = """
"""