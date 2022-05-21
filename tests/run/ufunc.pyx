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

def test_to_the_power():
    """
    >>> np.allclose(to_the_power(double_arr_1d, 1.), double_arr_1d)
    True
    >>> np.allclose(to_the_power(1., double_arr_2d), np.ones_like(double_arr_2d))
    True
    """

@cython.ufunc
cdef object py_return_value(double x):
    if x >= 0:
        return x
    # else we forget to set it and trigger an error

def test_py_return_value():
    """
    >>> py_return_value(5.)
    5.0
    >>> py_return_value(double_arr_1d).dtype
    dtype('O')
    >>> py_return_value(-1.)
    Traceback (most recent call last):
    ...
    ValueError: Python object output was not set
    """

@cython.ufunc
cdef double py_arg(object x):
    return float(x)

def test_py_arg():
    """
    >>> py_arg(np.array([1, "2.0", 3.0], dtype=object))
    array([1., 2., 3.])
    """

@cython.ufunc
cdef (double, long) multiple_return_values(long x):
    return x*1.5, x*2

@cython.ufunc
cdef (double, long) multiple_return_values2(long x):
    inefficient_tuple_intermediate = (x*1.5, x*2)
    return inefficient_tuple_intermediate

def test_multiple_return_values():
    """
    >>> multiple_return_values(int_arr_1d)
    (array([ 0.,  6., 12., 18., 24.]), array([ 0,  8, 16, 24, 32]))
    >>> multiple_return_values2(int_arr_1d)
    (array([ 0.,  6., 12., 18., 24.]), array([ 0,  8, 16, 24, 32]))
    """

@cython.ufunc
cdef cython.numeric plus_one(cython.numeric x):
    return x+1

def test_plus_one():
    """
    This generates all the fused combinations
    >>> plus_one(int_arr_1d)
    array([ 1,  5,  9, 13, 17])
    >>> plus_one(double_arr_2d)
    array([[57., 58.],
           [67., 68.],
           [77., 78.]])
    >>> plus_one(1.j)
    (1+1j)
    """

###### Test flow-control ######
# The transformation to a ufunc changes return statements to assignments and a break
# These tests make sure that it's working correctly

@cython.ufunc
cdef double return_stops_execution(double x):
    return x
    print "This should not happen"

@cython.ufunc
cdef double return_in_if(double x):
    if x<0:
        return -x
    return x

@cython.ufunc
cdef double nested_loops(double x):
    cdef double counter=0
    while x>counter:
        counter+=10.
        for i in range(100):
            if i>x:
                return i
    return x-counter

def test_flow_control():
    """
    >>> np.allclose(return_stops_execution(double_arr_1d), double_arr_1d)
    True
    >>> return_in_if(-1.)
    1.0
    >>> return_in_if(2.0)
    2.0
    >>> nested_loops(5.5)
    6.0
    >>> nested_loops(105.)
    -5.0
    """
