# mode: run
# tag: numpy

"""
Test accepting NumPy arrays with arbitrary strides for zero- or one-sized
dimensions.

Thanks to Nathaniel Smith and Sebastian Berg.

See also:

    Mailing list threads:
      http://thread.gmane.org/gmane.comp.python.cython.devel/14762
      http://thread.gmane.org/gmane.comp.python.cython.devel/14634

    Detailed discussion of the difference between numpy/cython's current
    definition of "contiguity", and the correct definition:
      http://thread.gmane.org/gmane.comp.python.cython.devel/14634/focus=14640

    The PR implementing NPY_RELAXED_STRIDES_CHECKING:
      https://github.com/numpy/numpy/pull/3162

    Another test case:
      https://github.com/numpy/numpy/issues/2956
"""

import numpy as np

numpy_version = np.__version__.split('.')[:2]
try:
    numpy_version = tuple(map(int, numpy_version))
except ValueError:
    numpy_version = (20, 0)

NUMPY_HAS_RELAXED_STRIDES = (
    numpy_version < (1, 8) or
    np.ones((10, 1), order="C").flags.f_contiguous)


def test_one_sized(array):
    """
    >>> contig = np.ascontiguousarray(np.arange(10, dtype=np.double)[::100])
    >>> test_one_sized(contig)[0]
    1.0
    >>> a = np.arange(10, dtype=np.double)[::100]
    >>> if NUMPY_HAS_RELAXED_STRIDES: print(test_one_sized(a)[0])
    ... else: print(1.0)
    1.0
    """
    cdef double[::1] a = array
    a[0] += 1.
    return array


def test_zero_sized(array):
    """
    >>> contig = np.ascontiguousarray(np.arange(10, dtype=np.double)[100:200:10])
    >>> _ = test_zero_sized(contig)

    >>> a = np.arange(10, dtype=np.double)[100:200:10]
    >>> if NUMPY_HAS_RELAXED_STRIDES: _ = test_zero_sized(a)
    """
    cdef double[::1] a = array
    return a
