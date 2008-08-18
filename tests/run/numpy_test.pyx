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
    <_BLANKLINE_>
     [[  8.   9.  10.  11.]
      [ 12.  13.  14.  15.]]
    <_BLANKLINE_>
     [[ 16.  17.  18.  19.]
      [ 20.  21.  22.  23.]]]
    6.0 0.0 13.0 8.0
    
    >>> obj_array()
    [a 1 {}]
    a 1 {}

    Test various forms of slicing, picking etc.
    >>> a = np.arange(10, dtype='l').reshape(2, 5)
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
    >>> print_long_2d(a[:, 1:5:2])
    1 3
    6 8
    >>> print_long_2d(a[:, 5:1:-2])
    4 2
    9 7
    >>> print_long_2d(a[:, [3, 1]])
    3 1
    8 6
    >>> print_long_2d(a.T)
    0 5
    1 6
    2 7
    3 8
    4 9

    Write to slices
    >>> b = a.copy()
    >>> put_range_long_1d(b[:, 3])
    >>> print b
    [[0 1 2 0 4]
     [5 6 7 1 9]]
    >>> put_range_long_1d(b[::-1, 3])
    >>> print b
    [[0 1 2 1 4]
     [5 6 7 0 9]]
    >>> a = np.zeros(9, dtype='l')
    >>> put_range_long_1d(a[1::3])
    >>> print a
    [0 0 0 0 1 0 0 2 0]

    Write to picked subarrays. This should NOT change the original
    array as picking creates a new mutable copy.
    >>> a = np.zeros(10, dtype='l').reshape(2, 5)
    >>> put_range_long_1d(a[[0, 0, 1, 1, 0], [0, 1, 2, 4, 3]])
    >>> print a
    [[0 0 0 0 0]
     [0 0 0 0 0]]
    
    >>> test_dtype('b', inc1_byte)
    >>> test_dtype('B', inc1_ubyte)
    >>> test_dtype('h', inc1_short)
    >>> test_dtype('H', inc1_ushort)
    >>> test_dtype('i', inc1_int)
    >>> test_dtype('I', inc1_uint)
    >>> test_dtype('l', inc1_long)
    >>> test_dtype('L', inc1_ulong)
    >>> test_dtype('f', inc1_float)
    >>> test_dtype('d', inc1_double)
    >>> test_dtype('g', inc1_longdouble)
    >>> test_dtype('O', inc1_object)

    >>> test_dtype(np.int, inc1_int_t)
    >>> test_dtype(np.long, inc1_long_t)
    >>> test_dtype(np.float, inc1_float_t)
    >>> test_dtype(np.double, inc1_double_t)

    >>> test_dtype(np.longdouble, inc1_longdouble_t)

    >>> test_dtype(np.int32, inc1_int32_t)
    >>> test_dtype(np.float64, inc1_float64_t)

    Unsupported types:
    >>> test_dtype(np.complex, inc1_byte)
    Traceback (most recent call last):
       ...
    ValueError: only objects, int and float dtypes supported for ndarray buffer access so far (dtype is 15)

    >>> a = np.zeros((10,), dtype=np.dtype('i4,i4'))
    >>> inc1_byte(a)
    Traceback (most recent call last):
       ...
    ValueError: only objects, int and float dtypes supported for ndarray buffer access so far (dtype is 20)
    
"""
except:
    __doc__ = ""

def ndarray_str(arr):
    """
    Since Py2.3 doctest don't support <BLANKLINE>, manually replace blank lines
    with <_BLANKLINE_>
    """
    return str(arr).replace('\n\n', '\n<_BLANKLINE_>\n')    

def basic():
    cdef object[int, ndim=2] buf = np.arange(10, dtype='i').reshape((2, 5))
    print buf
    print buf[0, 2], buf[0, 0], buf[1, 4], buf[1, 0]

def three_dim():
    cdef object[double, ndim=3] buf = np.arange(24, dtype='d').reshape((3,2,4))
    print ndarray_str(buf)
    print buf[0, 1, 2], buf[0, 0, 0], buf[1, 1, 1], buf[1, 0, 0]

def obj_array():
    cdef object[object, ndim=1] buf = np.array(["a", 1, {}])
    print buf
    print buf[0], buf[1], buf[2]


def print_long_2d(np.ndarray[long, ndim=2] arr):
    cdef int i, j
    for i in range(arr.shape[0]):
        print " ".join([str(arr[i, j]) for j in range(arr.shape[1])])

def put_range_long_1d(np.ndarray[long] arr):
    """Writes 0,1,2,... to array and returns array"""
    cdef int value = 0, i
    for i in range(arr.shape[0]):
        arr[i] = value
        value += 1


# Exhaustive dtype tests -- increments element [1] by 1 for all dtypes
def inc1_byte(np.ndarray[char] arr):                    arr[1] += 1
def inc1_ubyte(np.ndarray[unsigned char] arr):          arr[1] += 1
def inc1_short(np.ndarray[short] arr):                  arr[1] += 1
def inc1_ushort(np.ndarray[unsigned short] arr):        arr[1] += 1
def inc1_int(np.ndarray[int] arr):                      arr[1] += 1
def inc1_uint(np.ndarray[unsigned int] arr):            arr[1] += 1
def inc1_long(np.ndarray[long] arr):                    arr[1] += 1
def inc1_ulong(np.ndarray[unsigned long] arr):          arr[1] += 1
def inc1_longlong(np.ndarray[long long] arr):           arr[1] += 1
def inc1_ulonglong(np.ndarray[unsigned long long] arr): arr[1] += 1

def inc1_float(np.ndarray[float] arr):                  arr[1] += 1
def inc1_double(np.ndarray[double] arr):                arr[1] += 1
def inc1_longdouble(np.ndarray[long double] arr):       arr[1] += 1


def inc1_object(np.ndarray[object] arr):
    o = arr[1]
    o += 1
    arr[1] = o # unfortunately, += segfaults for objects


def inc1_int_t(np.ndarray[np.int_t] arr):               arr[1] += 1
def inc1_long_t(np.ndarray[np.long_t] arr):             arr[1] += 1
def inc1_float_t(np.ndarray[np.float_t] arr):           arr[1] += 1
def inc1_double_t(np.ndarray[np.double_t] arr):         arr[1] += 1
def inc1_longdouble_t(np.ndarray[np.longdouble_t] arr): arr[1] += 1

# The tests below only work on platforms that has the given types
def inc1_int32_t(np.ndarray[np.int32_t] arr):           arr[1] += 1
def inc1_float64_t(np.ndarray[np.float64_t] arr):       arr[1] += 1

    
def test_dtype(dtype, inc1):
    a = np.array([0, 10], dtype=dtype)
    inc1(a)
    if a[1] != 11: print "failed!"
