# mode: run
# tag: numpy

cimport numpy as np
cimport cython

import numpy as np

import re


def little_endian():
    cdef int endian_detector = 1
    return (<char*>&endian_detector)[0] != 0


def testcase(f):
    # testcase decorator now does nothing (following changes to doctest)
    # but is a useful indicator of what functions are designed as tests
    return f


if little_endian():
    my_endian = '<'
    other_endian = '>'
else:
    my_endian = '>'
    other_endian = '<'


def assert_dtype_sizes():
    """
    >>> assert_dtype_sizes()
    """
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


@testcase
def test_enums():
    """
    >>> test_enums()
    """
    cdef np.NPY_CASTING nc = np.NPY_NO_CASTING
    assert nc != np.NPY_SAFE_CASTING


def ndarray_str(arr):
    u"""
    Work around display differences in NumPy 1.14.
    """
    return re.sub(ur'\[ +', '[', unicode(arr))


def basic():
    """
    >>> basic()
    [[0 1 2 3 4]
     [5 6 7 8 9]]
    2 0 9 5
    """
    cdef object[int, ndim=2] buf = np.arange(10, dtype='i').reshape((2, 5))
    print buf
    print buf[0, 2], buf[0, 0], buf[1, 4], buf[1, 0]


def three_dim():
    """
    >>> three_dim()  # doctest: +NORMALIZE_WHITESPACE
    [[[0.   1.   2.   3.]
      [4.   5.   6.   7.]]
    <BLANKLINE>
     [[8.   9.  10.  11.]
      [12.  13.  14.  15.]]
    <BLANKLINE>
     [[16.  17.  18.  19.]
      [20.  21.  22.  23.]]]
    6.0 0.0 13.0 8.0
    """
    cdef object[double, ndim=3] buf = np.arange(24, dtype='d').reshape((3,2,4))
    print ndarray_str(buf)
    print buf[0, 1, 2], buf[0, 0, 0], buf[1, 1, 1], buf[1, 0, 0]


def obj_array():
    """
    >>> obj_array()
    [a 1 {}]
    a 1 {}
    """
    cdef object[object, ndim=1] buf = np.array(["a", 1, {}])
    print str(buf).replace('"', '').replace("'", '')
    print buf[0], buf[1], buf[2]


def print_long_2d(np.ndarray[long, ndim=2] arr):
    """
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
    """
    cdef int i, j
    for i in range(arr.shape[0]):
        print u" ".join([unicode(arr[i, j]) for j in range(arr.shape[1])])


def put_range_long_1d(np.ndarray[long] arr):
    """
    Write to slices
    >>> b = np.arange(10, dtype='l').reshape(2, 5)
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
    """
    # Writes 0,1,2,... to array and returns array
    cdef int value = 0, i
    for i in range(arr.shape[0]):
        arr[i] = value
        value += 1


def test_c_contig(np.ndarray[int, ndim=2, mode='c'] arr):
    """
    Test contiguous access modes:
    >>> c_arr = np.array(np.arange(12, dtype='i').reshape(3,4), order='C')
    >>> f_arr = np.array(np.arange(12, dtype='i').reshape(3,4), order='F')
    >>> test_c_contig(c_arr)
    0 1 2 3
    4 5 6 7
    8 9 10 11
    >>> test_c_contig(f_arr) #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ndarray is not C...contiguous
    >>> test_c_contig(c_arr[::2,::2]) #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ndarray is not C...contiguous
    """
    cdef int i, j
    for i in range(arr.shape[0]):
        print u" ".join([unicode(arr[i, j]) for j in range(arr.shape[1])])


def test_f_contig(np.ndarray[int, ndim=2, mode='fortran'] arr):
    """
    Test contiguous access modes:
    >>> c_arr = np.array(np.arange(12, dtype='i').reshape(3,4), order='C')
    >>> f_arr = np.array(np.arange(12, dtype='i').reshape(3,4), order='F')
    >>> test_f_contig(f_arr)
    0 1 2 3
    4 5 6 7
    8 9 10 11
    >>> test_f_contig(c_arr) #doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: ndarray is not Fortran contiguous
    """
    cdef int i, j
    for i in range(arr.shape[0]):
        print u" ".join([unicode(arr[i, j]) for j in range(arr.shape[1])])


# Exhaustive dtype tests -- increments element [1] by 1 (or 1+1j) for all dtypes
def inc1_bool(np.ndarray[unsigned char] arr):           arr[1] += 1
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
    """
    >>> test_dtype('?', inc1_bool)
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

    >>> test_dtype(np.int_, inc1_int_t)
    >>> test_dtype(np.longlong, inc1_longlong_t)
    >>> test_dtype(np.float_, inc1_float_t)
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
    """
    if dtype in ("g", np.longdouble,
                 "G", np.clongdouble):
        if sizeof(double) == sizeof(long double): # MSVC
            return
    if dtype in ('F', 'D', 'G'):
        a = np.array([0, 10+10j], dtype=dtype)
        inc1(a)
        if a[1] != (11 + 11j): print u"failed!", a[1]
    elif dtype == '?':
        # bool ndarrays coerce all values to 0 or 1
        a = np.array([0, 0], dtype=dtype)
        inc1(a)
        if a[1] != 1: print u"failed!"
        inc1(a)
        if a[1] != 1: print u"failed!"
    else:
        a = np.array([0, 10], dtype=dtype)
        inc1(a)
        if a[1] != 11: print u"failed!"


cdef struct DoubleInt:
    int x, y

def test_recordarray():
    """
    >>> test_recordarray()
    """
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
    """
    >>> print(test_nested_dtypes(np.zeros((3,), dtype=np.dtype([\
            ('a', np.dtype('i,i')),\
            ('b', np.dtype('i,i'))\
        ]))))                              # doctest: +NORMALIZE_WHITESPACE
    array([((0, 0), (0, 0)), ((1, 2), (1, 4)), ((1, 2), (1, 4))],
          dtype=[('a', [('f0', '!i4'), ('f1', '!i4')]), ('b', [('f0', '!i4'), ('f1', '!i4')])])

    >>> print(test_nested_dtypes(np.zeros((3,), dtype=np.dtype([\
            ('a', np.dtype('i,f')),\
            ('b', np.dtype('i,i'))\
        ]))))
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch, expected 'int' but got 'float' in 'DoubleInt.y'
    """
    cdef object[NestedStruct] arr = obj
    arr[1].a.x = 1
    arr[1].a.y = 2
    arr[1].b.x = arr[0].a.y + 1
    arr[1].b.y = 4
    arr[2] = arr[1]
    return repr(arr).replace('<', '!').replace('>', '!')


def test_bad_nested_dtypes():
    """
    >>> test_bad_nested_dtypes()
    """
    cdef object[BadNestedStruct] arr


def test_good_cast():
    """
    >>> test_good_cast()
    True
    """
    # Check that a signed int can round-trip through casted unsigned int access
    cdef np.ndarray[unsigned int, cast=True] arr = np.array([-100], dtype='i')
    cdef unsigned int data = arr[0]
    return -100 == <int>data


def test_bad_cast():
    """
    >>> test_bad_cast()
    Traceback (most recent call last):
        ...
    ValueError: Item size of buffer (1 byte) does not match size of 'int' (4 bytes)
    """
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
    """
    >>> print(test_packed_align(np.zeros((1,), dtype=np.dtype('b,i', align=False))))
    [(22, 23)]
    >>> print(test_packed_align(np.zeros((1,), dtype=np.dtype('b,i', align=True)))) #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    """
    arr[0].a = 22
    arr[0].b = 23
    return list(arr)


def test_unpacked_align(np.ndarray[UnpackedStruct] arr):
    """
    The output changed in Python 3:
    >> print(test_unpacked_align(np.zeros((1,), dtype=np.dtype('b,i', align=True))))
    array([(22, 23)],
          dtype=[('f0', '|i1'), ('', '|V3'), ('f1', '!i4')])

    ->

    array([(22, 23)],
          dtype={'names':['f0','f1'], 'formats':['i1','!i4'], 'offsets':[0,4], 'itemsize':8, 'aligned':True})


    >>> print(test_unpacked_align(np.zeros((1,), dtype=np.dtype('b,i', align=True))))
    [(22, 23)]
    >>> print(test_unpacked_align(np.zeros((1,), dtype=np.dtype('b,i', align=False)))) #doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    """
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
    """
    >>> test_complextypes()
    1,1
    1,1
    8,16
    """
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
    """
    >>> test_point_record()         # doctest: +NORMALIZE_WHITESPACE
    array([(0., 0.), (1., -1.), (2., -2.)],
          dtype=[('x', '!f8'), ('y', '!f8')])
    """
    cdef np.ndarray[Point] test
    Point_dtype = np.dtype([('x', np.float64), ('y', np.float64)])
    test = np.zeros(3, Point_dtype)
    cdef int i
    for i in range(3):
        test[i].x = i
        test[i].y = -i
    print re.sub(
        r'\.0+\b', '.', repr(test).replace('<', '!').replace('>', '!')
                                  .replace('( ', '(').replace(',  ', ', '))


# Test fused np.ndarray dtypes and runtime dispatch
@testcase
def test_fused_ndarray_floating_dtype(np.ndarray[cython.floating, ndim=1] a):
    """
    >>> import cython
    >>> sorted(test_fused_ndarray_floating_dtype.__signatures__)
    ['double', 'float']


    >>> test_fused_ndarray_floating_dtype[cython.double](np.arange(10, dtype=np.float64))
    ndarray[double,ndim=1] ndarray[double,ndim=1] 5.0 6.0
    >>> test_fused_ndarray_floating_dtype(np.arange(10, dtype=np.float64))
    ndarray[double,ndim=1] ndarray[double,ndim=1] 5.0 6.0

    >>> test_fused_ndarray_floating_dtype[cython.float](np.arange(10, dtype=np.float32))
    ndarray[float,ndim=1] ndarray[float,ndim=1] 5.0 6.0
    >>> test_fused_ndarray_floating_dtype(np.arange(10, dtype=np.float32))
    ndarray[float,ndim=1] ndarray[float,ndim=1] 5.0 6.0
    """
    cdef np.ndarray[cython.floating, ndim=1] b = a
    print cython.typeof(a), cython.typeof(b), a[5], b[6]


double_array = np.linspace(0, 1, 100)
int32_array = np.arange(100, dtype=np.int32)

cdef fused fused_external:
    np.int32_t
    np.int64_t
    np.float32_t
    np.float64_t


@testcase
def test_fused_external(np.ndarray[fused_external, ndim=1] a):
    """
    >>> import cython
    >>> sorted(test_fused_external.__signatures__)
    ['float32_t', 'float64_t', 'int32_t', 'int64_t']

    >>> test_fused_external["float64_t"](double_array)
    float64

    >>> test_fused_external["int32_t"](int32_array)
    int32

    >>> test_fused_external(np.arange(100, dtype=np.int64))
    int64
    """
    print a.dtype


cdef fused fused_buffers:
    np.ndarray[np.int32_t, ndim=1]
    np.int64_t[::1]

@testcase
def test_fused_buffers(fused_buffers arg):
    """
    >>> sorted(test_fused_buffers.__signatures__)
    ['int64_t[::1]', 'ndarray[int32_t,ndim=1]']
    """


cpdef _fused_cpdef_buffers(np.ndarray[fused_external] a):
    print a.dtype

@testcase
def test_fused_cpdef_buffers():
    """
    >>> test_fused_cpdef_buffers()
    int32
    int32
    """
    _fused_cpdef_buffers[np.int32_t](int32_array)

    cdef np.ndarray[np.int32_t] typed_array = int32_array
    _fused_cpdef_buffers(typed_array)


@testcase
def test_fused_ndarray_integral_dtype(np.ndarray[cython.integral, ndim=1] a):
    """
    >>> import cython
    >>> sorted(test_fused_ndarray_integral_dtype.__signatures__)
    ['int', 'long', 'short']

    >>> test_fused_ndarray_integral_dtype[cython.int](np.arange(10, dtype=np.dtype('i')))
    5 6
    >>> test_fused_ndarray_integral_dtype(np.arange(10, dtype=np.dtype('i')))
    5 6

    >>> test_fused_ndarray_integral_dtype[cython.long](np.arange(10, dtype='l'))
    5 6
    >>> test_fused_ndarray_integral_dtype(np.arange(10, dtype='l'))
    5 6
    """
    cdef np.ndarray[cython.integral, ndim=1] b = a
    # Don't print the types, the platform specific sizes can make the dispatcher
    # select different integer types with equal sizeof()
    print a[5], b[6]


cdef fused fused_dtype:
    float complex
    double complex
    object

@testcase
def test_fused_ndarray_other_dtypes(np.ndarray[fused_dtype, ndim=1] a):
    """
    >>> import cython
    >>> sorted(test_fused_ndarray_other_dtypes.__signatures__)
    ['double complex', 'float complex', 'object']
    >>> test_fused_ndarray_other_dtypes(np.arange(10, dtype=np.complex64))
    ndarray[float complex,ndim=1] ndarray[float complex,ndim=1] (5+0j) (6+0j)
    >>> test_fused_ndarray_other_dtypes(np.arange(10, dtype=np.complex128))
    ndarray[double complex,ndim=1] ndarray[double complex,ndim=1] (5+0j) (6+0j)
    >>> test_fused_ndarray_other_dtypes(np.arange(10, dtype=np.object_))
    ndarray[Python object,ndim=1] ndarray[Python object,ndim=1] 5 6
    """
    cdef np.ndarray[fused_dtype, ndim=1] b = a
    print cython.typeof(a), cython.typeof(b), a[5], b[6]


# Test fusing the array types together and runtime dispatch
cdef struct Foo:
    int a
    float b

cdef fused fused_FooArray:
    np.ndarray[Foo, ndim=1]

cdef fused fused_ndarray:
    np.ndarray[float, ndim=1]
    np.ndarray[double, ndim=1]
    np.ndarray[Foo, ndim=1]

def get_Foo_array():
    cdef Foo data[10]
    for i in range(10):
        data[i] = [0, 0]
    data[5].b = 9.0
    return np.asarray(<Foo[:]>data).copy()

def test_fused_ndarray(fused_ndarray a):
    """
    >>> import cython
    >>> sorted(test_fused_ndarray.__signatures__)
    ['ndarray[Foo,ndim=1]', 'ndarray[double,ndim=1]', 'ndarray[float,ndim=1]']

    >>> test_fused_ndarray(get_Foo_array())
    ndarray[Foo,ndim=1] ndarray[Foo,ndim=1]
    9.0
    >>> test_fused_ndarray(np.arange(10, dtype=np.float64))
    ndarray[double,ndim=1] ndarray[double,ndim=1]
    5.0
    >>> test_fused_ndarray(np.arange(10, dtype=np.float32))
    ndarray[float,ndim=1] ndarray[float,ndim=1]
    5.0
    """
    cdef fused_ndarray b = a
    print cython.typeof(a), cython.typeof(b)

    if fused_ndarray in fused_FooArray:
        print b[5].b
    else:
        print b[5]


cpdef test_fused_cpdef_ndarray(fused_ndarray a):
    """
    >>> import cython
    >>> sorted(test_fused_cpdef_ndarray.__signatures__)
    ['ndarray[Foo,ndim=1]', 'ndarray[double,ndim=1]', 'ndarray[float,ndim=1]']

    >>> test_fused_cpdef_ndarray(get_Foo_array())
    ndarray[Foo,ndim=1] ndarray[Foo,ndim=1]
    9.0
    >>> test_fused_cpdef_ndarray(np.arange(10, dtype=np.float64))
    ndarray[double,ndim=1] ndarray[double,ndim=1]
    5.0
    >>> test_fused_cpdef_ndarray(np.arange(10, dtype=np.float32))
    ndarray[float,ndim=1] ndarray[float,ndim=1]
    5.0
    """
    cdef fused_ndarray b = a
    print cython.typeof(a), cython.typeof(b)

    if fused_ndarray in fused_FooArray:
        print b[5].b
    else:
        print b[5]


def test_fused_cpdef_ndarray_cdef_call():
    """
    >>> test_fused_cpdef_ndarray_cdef_call()
    ndarray[Foo,ndim=1] ndarray[Foo,ndim=1]
    9.0
    """
    cdef np.ndarray[Foo, ndim=1] foo_array = get_Foo_array()
    test_fused_cpdef_ndarray(foo_array)


cdef fused int_type:
    np.int32_t
    np.int64_t

float64_array = np.arange(10, dtype=np.float64)
float32_array = np.arange(10, dtype=np.float32)
int32_array = np.arange(10, dtype=np.int32)
int64_array = np.arange(10, dtype=np.int64)

@testcase
def test_dispatch_non_clashing_declarations_repeating_types(np.ndarray[cython.floating] a1,
                                                            np.ndarray[int_type] a2,
                                                            np.ndarray[cython.floating] a3,
                                                            np.ndarray[int_type] a4):
    """
    >>> test_dispatch_non_clashing_declarations_repeating_types(float64_array, int32_array, float64_array, int32_array)
    1.0 2 3.0 4
    >>> test_dispatch_non_clashing_declarations_repeating_types(float64_array, int64_array, float64_array, int64_array)
    1.0 2 3.0 4
    >>> test_dispatch_non_clashing_declarations_repeating_types(float64_array, int32_array, float64_array, int64_array)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: Buffer dtype mismatch, expected 'int32_t'...
    >>> test_dispatch_non_clashing_declarations_repeating_types(float64_array, int64_array, float64_array, int32_array)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: Buffer dtype mismatch, expected 'int64_t'...
    """
    print a1[1], a2[2], a3[3], a4[4]


ctypedef np.int32_t typedeffed_type

cdef fused typedeffed_fused_type:
    typedeffed_type
    int
    long

@testcase
def test_dispatch_typedef(np.ndarray[typedeffed_fused_type] a):
    """
    >>> test_dispatch_typedef(int32_array)
    5
    """
    print a[5]


cdef extern from "types.h":
    ctypedef char actually_long_t

cdef fused confusing_fused_typedef:
    actually_long_t
    int
    unsigned long
    double complex
    unsigned char
    signed char

def test_dispatch_external_typedef(np.ndarray[confusing_fused_typedef] a):
    """
    >>> test_dispatch_external_typedef(np.arange(-5, 5, dtype=np.int_))
    -2
    """
    print a[3]


# test fused memoryview slices
cdef fused memslice_fused_dtype:
    float
    double
    int
    long
    float complex
    double complex
    object

@testcase
def test_fused_memslice_other_dtypes(memslice_fused_dtype[:] a):
    """
    >>> import cython
    >>> sorted(test_fused_memslice_other_dtypes.__signatures__)
    ['double', 'double complex', 'float', 'float complex', 'int', 'long', 'object']
    >>> test_fused_memslice_other_dtypes(np.arange(10, dtype=np.complex64))
    float complex[:] float complex[:] (5+0j) (6+0j)
    >>> test_fused_memslice_other_dtypes(np.arange(10, dtype=np.complex128))
    double complex[:] double complex[:] (5+0j) (6+0j)
    >>> test_fused_memslice_other_dtypes(np.arange(10, dtype=np.float32))
    float[:] float[:] 5.0 6.0
    >>> test_fused_memslice_other_dtypes(np.arange(10, dtype=np.dtype('i')))
    int[:] int[:] 5 6
    >>> test_fused_memslice_other_dtypes(np.arange(10, dtype=np.object_))
    object[:] object[:] 5 6
    """
    cdef memslice_fused_dtype[:] b = a
    print cython.typeof(a), cython.typeof(b), a[5], b[6]


cdef fused memslice_fused:
    float[:]
    double[:]
    int[:]
    long[:]
    float complex[:]
    double complex[:]
    object[:]

@testcase
def test_fused_memslice(memslice_fused a):
    """
    >>> import cython
    >>> sorted(test_fused_memslice.__signatures__)
    ['double complex[:]', 'double[:]', 'float complex[:]', 'float[:]', 'int[:]', 'long[:]', 'object[:]']
    >>> test_fused_memslice(np.arange(10, dtype=np.complex64))
    float complex[:] float complex[:] (5+0j) (6+0j)
    >>> test_fused_memslice(np.arange(10, dtype=np.complex128))
    double complex[:] double complex[:] (5+0j) (6+0j)
    >>> test_fused_memslice(np.arange(10, dtype=np.float32))
    float[:] float[:] 5.0 6.0
    >>> test_fused_memslice(np.arange(10, dtype=np.dtype('i')))
    int[:] int[:] 5 6
    >>> test_fused_memslice(np.arange(10, dtype=np.object_))
    object[:] object[:] 5 6
    """
    cdef memslice_fused b = a
    print cython.typeof(a), cython.typeof(b), a[5], b[6]


@testcase
def test_dispatch_memoryview_object():
    """
    >>> test_dispatch_memoryview_object()
    int[:] int[:] 5 6
    """
    cdef int[:] m = np.arange(10, dtype=np.dtype('i'))
    cdef int[:] m2 = m
    cdef int[:] m3 = <object> m
    test_fused_memslice(m3)


cdef fused ndim_t:
    double[:]
    double[:, :]
    double[:, :, :]

@testcase
def test_dispatch_ndim(ndim_t array):
    """
    >>> test_dispatch_ndim(np.empty(5, dtype=np.double))
    double[:] 1
    >>> test_dispatch_ndim(np.empty((5, 5), dtype=np.double))
    double[:, :] 2
    >>> test_dispatch_ndim(np.empty((5, 5, 5), dtype=np.double))
    double[:, :, :] 3

    Test indexing using Cython.Shadow
    >>> import cython
    >>> test_dispatch_ndim[cython.double[:]](np.empty(5, dtype=np.double))
    double[:] 1
    >>> test_dispatch_ndim[cython.double[:, :]](np.empty((5, 5), dtype=np.double))
    double[:, :] 2
    """
    print cython.typeof(array), np.asarray(array).ndim


@testcase
def test_copy_buffer(np.ndarray[double, ndim=1] a):
    """
    >>> a = test_copy_buffer(np.ones(10, dtype=np.double))
    >>> len(a)
    10
    >>> print(a.dtype)
    float64
    >>> a[0]
    1.0
    """
    a = a.copy()
    a = a.copy()
    a = a.copy()
    a = a.copy()
    a = a.copy()
    return a


@testcase
def test_broadcast_comparison(np.ndarray[double, ndim=1] a):
    """
    >>> a = np.ones(10, dtype=np.double)
    >>> a0, obj0, a1, obj1 = test_broadcast_comparison(a)
    >>> np.all(a0 == (a == 0)) or a0
    True
    >>> np.all(a1 == (a == 1)) or a1
    True
    >>> np.all(obj0 == (a == 0)) or obj0
    True
    >>> np.all(obj1 == (a == 1)) or obj1
    True

    >>> a = np.zeros(10, dtype=np.double)
    >>> a0, obj0, a1, obj1 = test_broadcast_comparison(a)
    >>> np.all(a0 == (a == 0)) or a0
    True
    >>> np.all(a1 == (a == 1)) or a1
    True
    >>> np.all(obj0 == (a == 0)) or obj0
    True
    >>> np.all(obj1 == (a == 1)) or obj1
    True
    """
    cdef object obj = a
    return a == 0, obj == 0, a == 1, obj == 1


@testcase
def test_c_api_searchsorted(np.ndarray arr, other):
    """
    >>> arr = np.random.randn(10)
    >>> other = np.random.randn(5)
    >>> result, expected = test_c_api_searchsorted(arr, other)
    >>> (result == expected).all()
    True
    """
    result = np.PyArray_SearchSorted(arr, other, np.NPY_SEARCHRIGHT, NULL)

    expected = arr.searchsorted(other, side="right")
    return result, expected
