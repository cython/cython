# mode: run
# tag: memoryview, cdivision, array

cimport cython
from cpython.array cimport array  # make Cython aware of the array type

def div_memoryview(int[:] A):
    """
    >>> from array import array
    >>> x = array('i', [6])
    >>> div_memoryview(x)
    >>> x[0]
    3
    """
    with cython.cdivision(True):
        A[0] /= 2

def div_buffer(object[int, ndim=1] A):
    """
    >>> from array import array
    >>> x = array('i', [6])
    >>> div_buffer(x)
    >>> x[0]
    3
    """
    with cython.cdivision(True):
        A[0] /= 2

