# mode: run
# tag: numpy

cimport cython

import numpy as np

# I'm making these arrays have slightly irregular strides deliberately
int_arr_1d = np.arange(20, dtype=int)[::4]
int_arr_2d = np.arange(500, dtype=int).reshape((50, -1))[5:8, 6:8]
double_arr_1d = int_arr_1d.astype(np.double)
double_arr_2d = int_arr_2d.astype(np.double)
# Numpy has a cutoff at about 500 where it releases the GIL, so test some large arrays
large_int_arr_1d = np.arange(1500, dtype=int)
large_int_arr_2d = np.arange(1500*600, dtype=int).reshape((1500, -1))
large_double_arr_1d = large_int_arr_1d.astype(np.double)
large_double_arr_2d = large_int_arr_2d.astype(np.double)

ctypedef double mydouble
ctypedef int myint
ctypedef double complex mycdouble

cdef extern from *:
    """
    typedef float someone_elses_float;
    typedef short someone_elses_int;
    typedef unsigned char someone_elses_unsigned_int;
    typedef signed long long someone_elses_signed_int;
    typedef signed int extern_actually_signed;
    typedef unsigned int extern_actually_unsigned;
    """
    ctypedef double someone_elses_float
    ctypedef int someone_elses_int
    ctypedef unsigned int someone_elses_unsigned_int
    ctypedef signed int someone_elses_signed_int
    ctypedef int extern_actually_signed
    ctypedef int extern_actually_unsigned

# it's fairly hard to test that nogil results in the GIL actually
# being released unfortunately
@cython.ufunc
cdef double triple_it(long x) nogil:
    """triple_it doc"""
    return x*3.

def test_triple_it():
    """
    Ufunc also generates a signature so just look at the end
    >>> triple_it.__doc__.endswith('triple_it doc')
    True
    >>> triple_it(int_arr_1d)
    array([ 0., 12., 24., 36., 48.])
    >>> triple_it(int_arr_2d)
    array([[168., 171.],
           [198., 201.],
           [228., 231.]])

    Treat the large arrays just as a "don't crash" test
    >>> _ = triple_it(large_int_arr_1d)
    >>> _ = triple_it(large_int_arr_2d)
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
    >>> _ = to_the_power(large_double_arr_1d, -large_double_arr_1d)
    >>> _ = to_the_power(large_double_arr_2d, -large_double_arr_2d)
    """

@cython.ufunc
cdef object py_return_value(double x):
    if x >= 0:
        return x
    # default returns None

def test_py_return_value():
    """
    >>> py_return_value(5.)
    5.0
    >>> py_return_value(double_arr_1d).dtype
    dtype('O')
    >>> py_return_value(-1.)  # returns None
    >>> _ = py_return_value(large_double_arr_1d)
    """

@cython.ufunc
cdef double py_arg(object x):
    return float(x)

def test_py_arg():
    """
    >>> py_arg(np.array([1, "2.0", 3.0], dtype=object))
    array([1., 2., 3.])
    >>> _ = py_arg(np.array([1]*1200, dtype=object))
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
    >>> plus_one(int_arr_1d)  # doctest: +ELLIPSIS
    array([ 1,  5,  9, 13, 17]...)
    >>> plus_one(double_arr_2d)
    array([[57., 58.],
           [67., 68.],
           [77., 78.]])
    >>> complex(plus_one(1.j))
    (1+1j)
    """

###### Test flow-control ######
# An initial implementation of ufunc did some odd restructuring of the code to
# bring the functions completely inline at the Cython level. These tests were to
# test that "return" statements work. They're less needed now, but don't do any
# harm

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
    >>> float(return_in_if(-1.))
    1.0
    >>> float(return_in_if(2.0))
    2.0
    >>> float(nested_loops(5.5))
    6.0
    >>> float(nested_loops(105.))
    -5.0
    """

@cython.ufunc
cdef double nested_function(double x):
    def f(x):
        return x*2
    return f(x)

def test_nested_function():
    """
    >>> np.allclose(nested_function(double_arr_1d), 2*double_arr_1d)
    True
    >>> float(nested_function(-1.))
    -2.0
    """

@cython.ufunc
cdef double can_throw(double x):
    if x<0:
        raise RuntimeError
    return x

def test_can_throw():
    """
    >>> arr = double_arr_1d.copy()
    >>> arr[1] = -1.
    >>> can_throw(arr)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> large_arr = large_double_arr_1d.copy()
    >>> large_arr[-4] = -2.
    >>> can_throw(large_arr)
    Traceback (most recent call last):
    ...
    RuntimeError
    >>> large_arr2d = large_double_arr_2d.copy()
    >>> large_arr2d[100, 200] = -1.
    >>> can_throw(large_arr2d)
    Traceback (most recent call last):
    ...
    RuntimeError
    """

@cython.ufunc
cdef mydouble known_typedefs(myint x, mycdouble y):
    return x*y.real*y.imag

def test_known_typedefs():
    """
    >>> known_typedefs(np.int32(3), 4+5j)
    60.0
    """

@cython.ufunc
cdef someone_elses_float unknown_typedefs(someone_elses_int x, someone_elses_signed_int y, someone_elses_unsigned_int z):
    return x+y+z

def test_unknown_typedefs():
    """
    >>> unknown_typedefs(np.short(1), np.longlong(3), np.uint8(2))
    6.0
    """

# really a compile-time test - should only generate one lot of utility code when working
# out what the Numpy type is.
@cython.ufunc
cdef double use_an_unknown_type_twice(someone_elses_float x, someone_elses_float y):
    return x * y

def test_use_twice():
    """
    >>> use_an_unknown_type_twice(2.0, 3.0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> use_an_unknown_type_twice(np.float32(2.0), np.float32(3.0))
    6.0
    """

ctypedef fused two_int_types:
    extern_actually_signed
    extern_actually_unsigned

@cython.ufunc
cdef object disambiguate_signedness(two_int_types x):
    return cython.typeof(x)

def test_disambiguate_asignedness():
    """
    >>> disambiguate_signedness(np.int32(-5))
    'extern_actually_signed'
    >>> disambiguate_signedness(np.uint32(10))
    'extern_actually_unsigned'
    """
