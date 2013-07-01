# tag: numpy
# mode: run

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

def test_one_sized(array):
    """
    >>> a = np.ascontiguousarray(np.arange(10, dtype=np.double)[::100])
    >>> test_one_sized(a)[0]
    1.0
    >>> a = np.arange(10, dtype=np.double)[::100]
    >>> test_one_sized(a)[0]
    1.0
    """
    cdef double[::1] a = array
    a[0] += 1.
    return array

def test_zero_sized(array):
    """
    >>> a = np.ascontiguousarray(np.arange(10, dtype=np.double)[100:200:10])
    >>> a = test_zero_sized(a)
    >>> a = np.arange(10, dtype=np.double)[100:200:10]
    >>> a = test_zero_sized(a)
    """
    cdef double[::1] a = array
    return a