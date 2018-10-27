# mode: run

cimport cython
@cython.boundscheck(False)
@cython.wraparound(False)
def testing_memoryview(double[:, :] x):
    """ Function testing boundscheck and wraparound in memoryview
    >>> import numpy as np
    >>> array = np.ones((2,2)) * 3.5
    >>> testing_memoryview(array)
    """
    cdef Py_ssize_t numrow = x.shape[0]
    cdef Py_ssize_t i
    for i in range(numrow):
        x[i, 0]
        x[i]
        x[i, ...]
        x[i, :]
