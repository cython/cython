# mode: run
# tag: numpy

cimport cython

import numpy as np

# I'm making these arrays have slightly irregular strides deliberately
int_arr_1d = np.arange(20, dtype=int)[::4]
int_arr_2d = np.arange(500, dtype=int).reshape((50, -1))[5:8, 6:8]
double_arr_1d = int_arr_1d.astype(np.double)
double_arr_2d = int_arr_2d.astype(np.double)

@cython.ufunc
cdef double tripple_it(long x):
    """tripple_it doc"""
    return x*3.

def test_tripple_it():
    """
    Ufunc also generates a signature so just look at the end
    >>> tripple_it.__doc__.endswith('tripple_it doc')
    True
    >>> tripple_it(int_arr_1d)
    array([ 0., 12., 24., 36., 48.])
    >>> tripple_it(int_arr_2d)
    array([[168., 171.],
           [198., 201.],
           [228., 231.]])
    """

@cython.ufunc
cdef double to_the_power(double x, double y):
    return x**y

@cython.ufunc
cdef object py_return_value(double x):
    return x

@cython.ufunc
cdef double py_arg(object x):
    return x

@cython.ufunc
cdef (double, int) multiple_return_values(int x):
    return x*1.5, x*2
