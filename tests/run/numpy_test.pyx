# tag: numpy
# cannot be named "numpy" in order to not clash with the numpy module!

cimport numpy as np

def little_endian():
    cdef int endian_detector = 1
    return (<char*>&endian_detector)[0] != 0

if little_endian():
    my_endian = '<'
    other_endian = '>'
else:
    my_endian = '>'
    other_endian = '<'

try:
    import numpy as np
    __doc__ = u"""

    >>> assert_dtype_sizes()

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
    >>> print (b)
    [[0 1 2 0 4]
     [5 6 7 1 9]]
    >>> put_range_long_1d(b[::-1, 3])
    >>> print (b)
    [[0 1 2 1 4]
     [5 6 7 0 9]]
    >>> a = np.zeros(9, dtype='l')
    >>> put_range_long_1d(a[1::3])
    >>> print (a)
    [0 0 0 0 1 0 0 2 0]

    Write to picked subarrays. This should NOT change the original
    array as picking creates a new mutable copy.
    >>> a = np.zeros(10, dtype='l').reshape(2, 5)
    >>> put_range_long_1d(a[[0, 0, 1, 1, 0], [0, 1, 2, 4, 3]])
    >>> print (a)
    [[0 0 0 0 0]
     [0 0 0 0 0]]

    Test contiguous access modes:
    >>> c_arr = np.array(np.arange(12, dtype='i').reshape(3,4), order='C')
    >>> f_arr = np.array(np.arange(12, dtype='i').reshape(3,4), order='F')
    >>> test_c_contig(c_arr)
    0 1 2 3
    4 5 6 7
    8 9 10 11
    >>> test_f_contig(f_arr)
    0 1 2 3
    4 5 6 7
    8 9 10 11
    >>> test_c_contig(f_arr) #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ndarray is not C...contiguous
    >>> test_f_contig(c_arr) #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ndarray is not Fortran contiguous
    >>> test_c_contig(c_arr[::2,::2]) #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ndarray is not C...contiguous
    
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
    >>> test_dtype('F', inc1_cfloat) # numpy format codes differ from buffer ones here
    >>> test_dtype('D', inc1_cdouble)
    >>> test_dtype('G', inc1_clongdouble)
    >>> test_dtype('F', inc1_cfloat_struct)
    >>> test_dtype('D', inc1_cdouble_struct)
    >>> test_dtype('G', inc1_clongdouble_struct)

    >>> test_dtype(np.int, inc1_int_t)
    >>> test_dtype(np.longlong, inc1_longlong_t)
    >>> test_dtype(np.float, inc1_float_t)
    >>> test_dtype(np.double, inc1_double_t)
    >>> test_dtype(np.intp, inc1_intp_t)
    >>> test_dtype(np.uintp, inc1_uintp_t)

    >>> test_dtype(np.longdouble, inc1_longdouble_t)

    >>> test_dtype(np.int32, inc1_int32_t)
    >>> test_dtype(np.float64, inc1_float64_t)

    Endian tests:
    >>> test_dtype('%si' % my_endian, inc1_int)
    >>> test_dtype('%si' % other_endian, inc1_int)  #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ...
    


    >>> test_recordarray()
    
    >>> print(test_nested_dtypes(np.zeros((3,), dtype=np.dtype([\
            ('a', np.dtype('i,i')),\
            ('b', np.dtype('i,i'))\
        ]))))
    array([((0, 0), (0, 0)), ((1, 2), (1, 4)), ((1, 2), (1, 4))], 
          dtype=[('a', [('f0', '!i4'), ('f1', '!i4')]), ('b', [('f0', '!i4'), ('f1', '!i4')])])

    >>> print(test_nested_dtypes(np.zeros((3,), dtype=np.dtype([\
            ('a', np.dtype('i,f')),\
            ('b', np.dtype('i,i'))\
        ]))))
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch, expected 'int' but got 'float' in 'DoubleInt.y'

    >>> print(test_packed_align(np.zeros((1,), dtype=np.dtype('b,i', align=False))))
    [(22, 23)]


    The output changed in Python 3:
    >> print(test_unpacked_align(np.zeros((1,), dtype=np.dtype('b,i', align=True))))
    array([(22, 23)], 
          dtype=[('f0', '|i1'), ('', '|V3'), ('f1', '!i4')])

    ->

    array([(22, 23)], 
          dtype={'names':['f0','f1'], 'formats':['i1','!i4'], 'offsets':[0,4], 'itemsize':8, 'aligned':True})


    >>> print(test_unpacked_align(np.zeros((1,), dtype=np.dtype('b,i', align=True))))
    [(22, 23)]

    >>> print(test_packed_align(np.zeros((1,), dtype=np.dtype('b,i', align=True)))) #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...

    >>> print(test_unpacked_align(np.zeros((1,), dtype=np.dtype('b,i', align=False)))) #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...


    >>> test_good_cast()
    True
    >>> test_bad_cast()
    Traceback (most recent call last):
        ...
    ValueError: Item size of buffer (1 byte) does not match size of 'int' (4 bytes)

    >>> test_complextypes()
    1,1
    1,1
    8,16

    >>> test_point_record()
    array([(0.0, 0.0), (1.0, -1.0), (2.0, -2.0)], 
          dtype=[('x', '!f8'), ('y', '!f8')])

"""

    if np.__version__ >= '1.6' and False:
        __doc__ += u"""
        Tests are DISABLED as the buffer format parser does not align members
        of aligned structs in padded structs in relation to the possibly
        unaligned initial offset.

        The following expose bugs in Numpy (versions prior to 2011-04-02):
        >>> print(test_partially_packed_align(np.zeros((1,), dtype=np.dtype([('a', 'b'), ('b', 'i'), ('sub', np.dtype('b,i')), ('c', 'i')], align=True))))
        array([(22, 23, (24, 25), 26)],
              dtype=[('a', '|i1'), ('', '|V3'), ('b', '!i4'), ('sub', [('f0', '|i1'), ('f1', '!i4')]), ('', '|V3'), ('c', '!i4')])

        >>> print(test_partially_packed_align_2(np.zeros((1,), dtype=np.dtype([('a', 'b'), ('b', 'i'), ('c', 'b'), ('sub', np.dtype('b,i', align=True))]))))
        array([(22, 23, 24, (27, 28))],
              dtype=[('a', '|i1'), ('b', '!i4'), ('c', '|i1'), ('sub', [('f0', '|i1'), ('', '|V3'), ('f1', '!i4')])])

        >>> print(test_partially_packed_align(np.zeros((1,), dtype=np.dtype([('a', 'b'), ('b', 'i'), ('sub', np.dtype('b,i')), ('c', 'i')], align=False)))) #doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: ...

        >>> print(test_partially_packed_align_2(np.zeros((1,), dtype=np.dtype([('a', 'b'), ('b', 'i'), ('c', 'b'), ('sub', np.dtype('b,i', align=False))])))) #doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: ...
        """

except:
    __doc__ = u""


def assert_dtype_sizes():
    assert sizeof(np.int8_t) == 1
    assert sizeof(np.int16_t) == 2
    assert sizeof(np.int32_t) == 4
    assert sizeof(np.int64_t) == 8
    assert sizeof(np.uint8_t) == 1
    assert sizeof(np.uint16_t) == 2
    assert sizeof(np.uint32_t) == 4
    assert sizeof(np.uint64_t) == 8
    assert sizeof(np.float32_t) == 4
    assert sizeof(np.float64_t) == 8
    assert sizeof(np.complex64_t) == 8
    assert sizeof(np.complex128_t) == 16

def ndarray_str(arr):
    u"""
    Since Py2.3 doctest don't support <BLANKLINE>, manually replace blank lines
    with <_BLANKLINE_>
    """
    return unicode(arr).replace(u'\n\n', u'\n<_BLANKLINE_>\n')

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
        print u" ".join([unicode(arr[i, j]) for j in range(arr.shape[1])])

def put_range_long_1d(np.ndarray[long] arr):
    u"""Writes 0,1,2,... to array and returns array"""
    cdef int value = 0, i
    for i in range(arr.shape[0]):
        arr[i] = value
        value += 1

def test_c_contig(np.ndarray[int, ndim=2, mode='c'] arr):
    cdef int i, j
    for i in range(arr.shape[0]):
        print u" ".join([unicode(arr[i, j]) for j in range(arr.shape[1])])

def test_f_contig(np.ndarray[int, ndim=2, mode='fortran'] arr):
    cdef int i, j
    for i in range(arr.shape[0]):
        print u" ".join([unicode(arr[i, j]) for j in range(arr.shape[1])])

# Exhaustive dtype tests -- increments element [1] by 1 (or 1+1j) for all dtypes
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

def inc1_cfloat(np.ndarray[float complex] arr):            arr[1] = arr[1] + 1 + 1j
def inc1_cdouble(np.ndarray[double complex] arr):          arr[1] = (arr[1] + 1) + 1j
def inc1_clongdouble(np.ndarray[long double complex] arr): arr[1] = arr[1] + (1 + 1j)

def inc1_cfloat_struct(np.ndarray[np.cfloat_t] arr):
    arr[1].real += 1
    arr[1].imag += 1
    
def inc1_cdouble_struct(np.ndarray[np.cdouble_t] arr):
    arr[1].real += 1
    arr[1].imag += 1

def inc1_clongdouble_struct(np.ndarray[np.clongdouble_t] arr):
    cdef long double x
    x = arr[1].real + 1
    arr[1].real = x
    arr[1].imag = arr[1].imag + 1

def inc1_object(np.ndarray[object] arr):
    o = arr[1]
    o += 1
    arr[1] = o # unfortunately, += segfaults for objects


def inc1_int_t(np.ndarray[np.int_t] arr):               arr[1] += 1
def inc1_long_t(np.ndarray[np.long_t] arr):             arr[1] += 1
def inc1_longlong_t(np.ndarray[np.longlong_t] arr):     arr[1] += 1
def inc1_float_t(np.ndarray[np.float_t] arr):           arr[1] += 1
def inc1_double_t(np.ndarray[np.double_t] arr):         arr[1] += 1
def inc1_longdouble_t(np.ndarray[np.longdouble_t] arr): arr[1] += 1
def inc1_intp_t(np.ndarray[np.intp_t] arr):             arr[1] += 1
def inc1_uintp_t(np.ndarray[np.uintp_t] arr):           arr[1] += 1

# The tests below only work on platforms that has the given types
def inc1_int32_t(np.ndarray[np.int32_t] arr):           arr[1] += 1
def inc1_float64_t(np.ndarray[np.float64_t] arr):       arr[1] += 1

    
def test_dtype(dtype, inc1):
    if dtype in ("g", np.longdouble,
                 "G", np.clongdouble):
        if sizeof(double) == sizeof(long double): # MSVC
            return
    if dtype in ('F', 'D', 'G'):
        a = np.array([0, 10+10j], dtype=dtype)
        inc1(a)
        if a[1] != (11 + 11j): print u"failed!", a[1]
    else:
        a = np.array([0, 10], dtype=dtype)
        inc1(a)
        if a[1] != 11: print u"failed!"

cdef struct DoubleInt:
    int x, y

def test_recordarray():
    cdef object[DoubleInt] arr
    arr = np.array([(5,5), (4, 6)], dtype=np.dtype('i,i'))
    cdef DoubleInt rec
    rec = arr[0]
    if rec.x != 5: print u"failed"
    if rec.y != 5: print u"failed"
    rec.y += 5
    arr[1] = rec
    arr[0].x -= 2
    arr[0].y += 3
    if arr[0].x != 3: print u"failed"
    if arr[0].y != 8: print u"failed"
    if arr[1].x != 5: print u"failed"
    if arr[1].y != 10: print u"failed"

cdef struct NestedStruct:
    DoubleInt a
    DoubleInt b

cdef struct BadDoubleInt:
    float x
    int y

cdef struct BadNestedStruct:
    DoubleInt a
    BadDoubleInt b

def test_nested_dtypes(obj):
    cdef object[NestedStruct] arr = obj
    arr[1].a.x = 1
    arr[1].a.y = 2
    arr[1].b.x = arr[0].a.y + 1
    arr[1].b.y = 4
    arr[2] = arr[1]
    return repr(arr).replace('<', '!').replace('>', '!')

def test_bad_nested_dtypes():
    cdef object[BadNestedStruct] arr

def test_good_cast():
    # Check that a signed int can round-trip through casted unsigned int access
    cdef np.ndarray[unsigned int, cast=True] arr = np.array([-100], dtype='i')
    cdef unsigned int data = arr[0]
    return -100 == <int>data

def test_bad_cast():
    # This should raise an exception
    cdef np.ndarray[int, cast=True] arr = np.array([1], dtype='b')

cdef packed struct PackedStruct:
    char a
    int b

cdef struct UnpackedStruct:
    char a
    int b

cdef struct PartiallyPackedStruct:
    char a
    int b
    PackedStruct sub
    int c

cdef packed struct PartiallyPackedStruct2:
    char a
    int b
    char c
    UnpackedStruct sub

def test_packed_align(np.ndarray[PackedStruct] arr):
    arr[0].a = 22
    arr[0].b = 23
    return list(arr)

def test_unpacked_align(np.ndarray[UnpackedStruct] arr):
    arr[0].a = 22
    arr[0].b = 23
    # return repr(arr).replace('<', '!').replace('>', '!')
    return list(arr)

def test_partially_packed_align(np.ndarray[PartiallyPackedStruct] arr):
    arr[0].a = 22
    arr[0].b = 23
    arr[0].sub.a = 24
    arr[0].sub.b = 25
    arr[0].c = 26
    return repr(arr).replace('<', '!').replace('>', '!')

def test_partially_packed_align_2(np.ndarray[PartiallyPackedStruct2] arr):
    arr[0].a = 22
    arr[0].b = 23
    arr[0].c = 24
    arr[0].sub.a = 27
    arr[0].sub.b = 28
    return repr(arr).replace('<', '!').replace('>', '!')

def test_complextypes():
    cdef np.complex64_t x64 = 1, y64 = 1j
    cdef np.complex128_t x128 = 1, y128 = 1j
    x64 = x64 + y64
    print "%.0f,%.0f" % (x64.real, x64.imag)
    x128 = x128 + y128
    print "%.0f,%.0f" % (x128.real, x128.imag)
    print "%d,%d" % (sizeof(x64), sizeof(x128))


cdef struct Point:
    np.float64_t x, y

def test_point_record():
    cdef np.ndarray[Point] test
    Point_dtype = np.dtype([('x', np.float64), ('y', np.float64)])
    test = np.zeros(3, Point_dtype)
    cdef int i
    for i in range(3):
        test[i].x = i
        test[i].y = -i
    print repr(test).replace('<', '!').replace('>', '!')

include "numpy_common.pxi"
