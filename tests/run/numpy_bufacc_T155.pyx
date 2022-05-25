# ticket: t155
# tag: numpy

"""
>>> myfunc()
0.5
"""

cimport numpy as np
import numpy as np

def myfunc():
    cdef np.ndarray[float, ndim=2] A = np.ones((1,1), dtype=np.float32)
    cdef int i

    for i from 0 <= i < A.shape[0]:
        A[i, :] /= 2
    return A[0,0]

