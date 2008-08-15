# cannot be named "numpy" in order to not clash with the numpy module!

cimport numpy as np

try:
    import numpy as np
    __doc__ = """

    >>> basic()
    [[0 1 2 3 4]
     [5 6 7 8 9]]
    2 0 9 5

    >>> three_dim()
    [[[  0.   1.   2.   3.]
      [  4.   5.   6.   7.]]
    <BLANKLINE>
     [[  8.   9.  10.  11.]
      [ 12.  13.  14.  15.]]
    <BLANKLINE>
     [[ 16.  17.  18.  19.]
      [ 20.  21.  22.  23.]]]
    6.0 0.0 13.0 8.0
    
    >>> obj_array()
    [a 1 {}]
    a 1 {}

    Test various forms of slicing, picking etc.
    >>> a = np.arange(10, dtype=np.long).reshape(2, 5)
    >>> print_long_2d(a)
    0 1 2 3 4
    5 6 7 8 9
    >>> print_long_2d(a[::-1, ::-1])
    9 8 7 6 5
    4 3 2 1 0
    >>> print_long_2d(a[1:2, 1:3])
    6 7
    >>> print_long_2d(a[::2, ::2])
    0 2 4
    >>> print_long_2d(a[::4, :])
    0 1 2 3 4
    >>> print_long_2d(a[4:1:-1, :])
    4 3 2
    
"""
except:
    __doc__ = ""

def basic():
    cdef object[int, ndim=2] buf = np.arange(10, dtype='i').reshape((2, 5))
    print buf
    print buf[0, 2], buf[0, 0], buf[1, 4], buf[1, 0]

def three_dim():
    cdef object[double, ndim=3] buf = np.arange(24, dtype='d').reshape((3,2,4))
    print buf
    print buf[0, 1, 2], buf[0, 0, 0], buf[1, 1, 1], buf[1, 0, 0]

def obj_array():
    cdef object[object, ndim=1] buf = np.array(["a", 1, {}])
    print buf
    print buf[0], buf[1], buf[2]


def print_long_2d(np.ndarray[long, 2] arr):
    cdef int i, j
    for i in range(arr.shape[0]):
        print " ".join([arr[i, j] for j in range(arr.shape[1])])
