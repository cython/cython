# tag: numpy
# mode: run

from cpython.object cimport Py_EQ

import sys

cimport numpy as np
import numpy as np

__test__ = {}

def testcase(f):
    assert f.__doc__, f
    __test__[f.__name__] = f.__doc__
    return f

def testcase_like(similar_func):
    def decorator(wrapper_func):
        assert similar_func.__doc__
        wrapper_func.__doc__ = similar_func.__doc__.replace(
                    similar_func.__name__, wrapper_func.__name__)
        return testcase(wrapper_func)
    return decorator

@testcase
def test_simple_binop_assign(int[:] m):
    """
    >>> a = np.arange(10, dtype='i')
    >>> np.asarray(test_simple_binop_assign(a))
    array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81], dtype=int32)
    """
    m[:] = m * m
    return m

@testcase
def test_simple_binop_assign_contig(int[::1] m):
    """
    >>> a = np.arange(10, dtype='i')
    >>> np.asarray(test_simple_binop_assign_contig(a))
    array([ 0,  1,  4,  9, 16, 25, 36, 49, 64, 81], dtype=int32)
    """
    m[:] = m * m
    return m

@testcase
def test_simple_binop_assign_2d(int[:, :] m):
    """
    >>> a2d = np.arange(100, dtype='i').reshape(10, 10)
    >>> np.asarray(test_simple_binop_assign_2d(a2d))
    array([[  0,   3,   6,   9,  12,  15,  18,  21,  24,  27],
           [ 30,  33,  36,  39,  42,  45,  48,  51,  54,  57],
           [ 60,  63,  66,  69,  72,  75,  78,  81,  84,  87],
           [ 90,  93,  96,  99, 102, 105, 108, 111, 114, 117],
           [120, 123, 126, 129, 132, 135, 138, 141, 144, 147],
           [150, 153, 156, 159, 162, 165, 168, 171, 174, 177],
           [180, 183, 186, 189, 192, 195, 198, 201, 204, 207],
           [210, 213, 216, 219, 222, 225, 228, 231, 234, 237],
           [240, 243, 246, 249, 252, 255, 258, 261, 264, 267],
           [270, 273, 276, 279, 282, 285, 288, 291, 294, 297]], dtype=int32)
    """
    m[:] = m + m + m
    return m

@testcase
def test_simple_binop_assign_contig_2d(int[:, :] m):
    """
    >>> a2d = np.arange(100, dtype='i').reshape(10, 10)
    >>> np.asarray(test_simple_binop_assign_contig_2d(a2d))
    array([[  0,   3,   6,   9,  12,  15,  18,  21,  24,  27],
           [ 30,  33,  36,  39,  42,  45,  48,  51,  54,  57],
           [ 60,  63,  66,  69,  72,  75,  78,  81,  84,  87],
           [ 90,  93,  96,  99, 102, 105, 108, 111, 114, 117],
           [120, 123, 126, 129, 132, 135, 138, 141, 144, 147],
           [150, 153, 156, 159, 162, 165, 168, 171, 174, 177],
           [180, 183, 186, 189, 192, 195, 198, 201, 204, 207],
           [210, 213, 216, 219, 222, 225, 228, 231, 234, 237],
           [240, 243, 246, 249, 252, 255, 258, 261, 264, 267],
           [270, 273, 276, 279, 282, 285, 288, 291, 294, 297]], dtype=int32)
    """
    m[:] = m + m + m
    return m

@testcase
def test_typedef(np.int32_t[:] m):
    """
    >>> np.asarray(test_typedef(np.arange(10, dtype=np.int32)))
    array([ 0,  3,  6,  9, 12, 15, 18, 21, 24, 27], dtype=int32)
    """
    m[:] = m + m + m
    return m

cdef fused fused_dtype_t:
    long
    long double
    double complex
    object

@testcase
def test_arbitrary_dtypes(fused_dtype_t[:] m1, fused_dtype_t[::1] m2):
    """
    >>> def operands(dtype):
    ...     return np.arange(10, dtype=dtype), np.arange(10, dtype=dtype)
    ...

    >>> test_arbitrary_dtypes(*operands('l'))
    array([ 0,  3,  6,  9, 12, 15, 18, 21, 24, 27])

    >>> test_arbitrary_dtypes(*operands(dtype=np.longdouble))
    array([ 0.0,  3.0,  6.0,  9.0,  12.0,  15.0,  18.0,  21.0,  24.0,  27.0], dtype=float128)

    >>> ops = operands(np.complex128)
    >>> test_arbitrary_dtypes(ops[0] + 1.2j, ops[1] + 1.2j)
    array([  0.+3.6j,   3.+3.6j,   6.+3.6j,   9.+3.6j,  12.+3.6j,  15.+3.6j,
            18.+3.6j,  21.+3.6j,  24.+3.6j,  27.+3.6j])

    >>> test_arbitrary_dtypes(*operands(dtype=np.object))
    array([0, 3, 6, 9, 12, 15, 18, 21, 24, 27], dtype=object)
    """
    m1[:] = m1 + m1 + m1
    m2[:] = m2 + m2 + m2
    assert np.all(np.asarray(m1) == np.asarray(m2)) or np.allclose(m1, m2)
    return np.asarray(m1)

cdef class UniqueObject(object):
    cdef public object value
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return UniqueObject(self.value + other.value)

    def __richcmp__(self, other, int opid):
        if opid == Py_EQ:
            return self.value == other.value
        return NotImplemented

    def __str__(self):
        return str(self.value)

    def __dealloc__(self):
        pass
        # sys.stdout.write("dealloc %s " % self.value)

class UniqueObjectInplace(UniqueObject):
    def __add__(self, other):
        self.value += other.value
        return self

def object_range(n, shape=None, cls=UniqueObject):
    result = np.array([cls(i) for i in range(n)], dtype=np.object)
    if shape:
        result = result.reshape(shape)
    return result

def test_broadcasting(fused_dtype_t[:] m1, fused_dtype_t[:, :] m2):
    """
    >>> def operands(dtype):
    ...     return np.arange(10, dtype=dtype), np.arange(100, dtype=dtype).reshape(10, 10)
    ...

    >>> test_broadcasting(*operands('l'))
    array([[  0,   2,   4,   6,   8,  10,  12,  14,  16,  18],
           [ 10,  12,  14,  16,  18,  20,  22,  24,  26,  28],
           [ 20,  22,  24,  26,  28,  30,  32,  34,  36,  38],
           [ 30,  32,  34,  36,  38,  40,  42,  44,  46,  48],
           [ 40,  42,  44,  46,  48,  50,  52,  54,  56,  58],
           [ 50,  52,  54,  56,  58,  60,  62,  64,  66,  68],
           [ 60,  62,  64,  66,  68,  70,  72,  74,  76,  78],
           [ 70,  72,  74,  76,  78,  80,  82,  84,  86,  88],
           [ 80,  82,  84,  86,  88,  90,  92,  94,  96,  98],
           [ 90,  92,  94,  96,  98, 100, 102, 104, 106, 108]])

    >>> test_broadcasting(*operands(np.complex128))
    array([[   0.+0.j,    2.+0.j,    4.+0.j,    6.+0.j,    8.+0.j,   10.+0.j,
              12.+0.j,   14.+0.j,   16.+0.j,   18.+0.j],
           [  10.+0.j,   12.+0.j,   14.+0.j,   16.+0.j,   18.+0.j,   20.+0.j,
              22.+0.j,   24.+0.j,   26.+0.j,   28.+0.j],
           [  20.+0.j,   22.+0.j,   24.+0.j,   26.+0.j,   28.+0.j,   30.+0.j,
              32.+0.j,   34.+0.j,   36.+0.j,   38.+0.j],
           [  30.+0.j,   32.+0.j,   34.+0.j,   36.+0.j,   38.+0.j,   40.+0.j,
              42.+0.j,   44.+0.j,   46.+0.j,   48.+0.j],
           [  40.+0.j,   42.+0.j,   44.+0.j,   46.+0.j,   48.+0.j,   50.+0.j,
              52.+0.j,   54.+0.j,   56.+0.j,   58.+0.j],
           [  50.+0.j,   52.+0.j,   54.+0.j,   56.+0.j,   58.+0.j,   60.+0.j,
              62.+0.j,   64.+0.j,   66.+0.j,   68.+0.j],
           [  60.+0.j,   62.+0.j,   64.+0.j,   66.+0.j,   68.+0.j,   70.+0.j,
              72.+0.j,   74.+0.j,   76.+0.j,   78.+0.j],
           [  70.+0.j,   72.+0.j,   74.+0.j,   76.+0.j,   78.+0.j,   80.+0.j,
              82.+0.j,   84.+0.j,   86.+0.j,   88.+0.j],
           [  80.+0.j,   82.+0.j,   84.+0.j,   86.+0.j,   88.+0.j,   90.+0.j,
              92.+0.j,   94.+0.j,   96.+0.j,   98.+0.j],
           [  90.+0.j,   92.+0.j,   94.+0.j,   96.+0.j,   98.+0.j,  100.+0.j,
             102.+0.j,  104.+0.j,  106.+0.j,  108.+0.j]])

    >>> result1 = test_broadcasting(object_range(10), object_range(100, (10, 10)))
    >>> result1
    array([[0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
           [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
           [20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
           [30, 32, 34, 36, 38, 40, 42, 44, 46, 48],
           [40, 42, 44, 46, 48, 50, 52, 54, 56, 58],
           [50, 52, 54, 56, 58, 60, 62, 64, 66, 68],
           [60, 62, 64, 66, 68, 70, 72, 74, 76, 78],
           [70, 72, 74, 76, 78, 80, 82, 84, 86, 88],
           [80, 82, 84, 86, 88, 90, 92, 94, 96, 98],
           [90, 92, 94, 96, 98, 100, 102, 104, 106, 108]], dtype=object)

    >>> result2 = test_broadcasting(object_range(10, cls=UniqueObjectInplace),
    ...                             object_range(100, (10, 10), cls=UniqueObjectInplace))
    >>> np.all(result1 == result2)
    True
    """
    m2[...] = m2 + m1
    return np.asarray(m2)

testcase(test_broadcasting)

#def test_broadcasting_c_contig(fused_dtype_t[::1] m1, fused_dtype_t[:, ::1] m2):
#    m2[...] = m2 + m1
#    return np.asarray(m2)

#testcase_like(test_broadcasting)(test_broadcasting_c_contig)
