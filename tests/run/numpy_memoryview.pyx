# tag: numpy
# mode: run

"""
Test slicing for memoryviews and memoryviewslices
"""

import sys

cimport numpy as np
import numpy as np
cimport cython

include "cythonarrayutil.pxi"
include "mockbuffers.pxi"

ctypedef np.int32_t dtype_t

def get_array():
    # We need to type our array to get a __pyx_get_buffer() that typechecks
    # for np.ndarray and calls __getbuffer__ in numpy.pxd
    cdef np.ndarray[dtype_t, ndim=3] a
    a = np.arange(8 * 14 * 11, dtype=np.int32).reshape(8, 14, 11)
    return a

a = get_array()

def ae(*args):
    "assert equals"
    for x in args:
        if x != args[0]:
            raise AssertionError(args)

__test__ = {}

def testcase(f):
    __test__[f.__name__] = f.__doc__
    return f

def testcase_numpy_1_5(f):
    major, minor, *rest = np.__version__.split('.')
    if (int(major), int(minor)) >= (1, 5):
        __test__[f.__name__] = f.__doc__
    return f

#
### Test slicing memoryview slices
#

@testcase
def test_partial_slicing(array):
    """
    >>> test_partial_slicing(a)
    """
    cdef dtype_t[:, :, :] a = array
    obj = array[4]

    cdef dtype_t[:, :] b = a[4, :]
    cdef dtype_t[:, :] c = a[4]

    ae(b.shape[0], c.shape[0], obj.shape[0])
    ae(b.shape[1], c.shape[1], obj.shape[1])
    ae(b.strides[0], c.strides[0], obj.strides[0])
    ae(b.strides[1], c.strides[1], obj.strides[1])

@testcase
def test_ellipsis(array):
    """
    >>> test_ellipsis(a)
    """
    cdef dtype_t[:, :, :] a = array

    cdef dtype_t[:, :] b = a[..., 4]
    b_obj = array[..., 4]

    cdef dtype_t[:, :] c = a[4, ...]
    c_obj = array[4, ...]

    cdef dtype_t[:, :] d = a[2:8, ..., 2]
    d_obj = array[2:8, ..., 2]

    ae(tuple([b.shape[i] for i in range(2)]), b_obj.shape)
    ae(tuple([b.strides[i] for i in range(2)]), b_obj.strides)
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            ae(b[i, j], b_obj[i, j])

    ae(tuple([c.shape[i] for i in range(2)]), c_obj.shape)
    ae(tuple([c.strides[i] for i in range(2)]), c_obj.strides)
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            ae(c[i, j], c_obj[i, j])

    ae(tuple([d.shape[i] for i in range(2)]), d_obj.shape)
    ae(tuple([d.strides[i] for i in range(2)]), d_obj.strides)
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ae(d[i, j], d_obj[i, j])

    cdef dtype_t[:] e = a[..., 5, 6]
    e_obj = array[..., 5, 6]
    ae(e.shape[0], e_obj.shape[0])
    ae(e.strides[0], e_obj.strides[0])

#
### Test slicing memoryview objects
#
@testcase
def test_partial_slicing_memoryview(array):
    """
    >>> test_partial_slicing_memoryview(a)
    """
    cdef dtype_t[:, :, :] _a = array
    a = _a
    obj = array[4]

    b = a[4, :]
    c = a[4]

    ae(b.shape[0], c.shape[0], obj.shape[0])
    ae(b.shape[1], c.shape[1], obj.shape[1])
    ae(b.strides[0], c.strides[0], obj.strides[0])
    ae(b.strides[1], c.strides[1], obj.strides[1])

@testcase
def test_ellipsis_memoryview(array):
    """
    >>> test_ellipsis_memoryview(a)
    """
    cdef dtype_t[:, :, :] _a = array
    a = _a

    b = a[..., 4]
    b_obj = array[..., 4]

    c = a[4, ...]
    c_obj = array[4, ...]

    d = a[2:8, ..., 2]
    d_obj = array[2:8, ..., 2]

    ae(tuple([b.shape[i] for i in range(2)]), b_obj.shape)
    ae(tuple([b.strides[i] for i in range(2)]), b_obj.strides)
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            ae(b[i, j], b_obj[i, j])

    ae(tuple([c.shape[i] for i in range(2)]), c_obj.shape)
    ae(tuple([c.strides[i] for i in range(2)]), c_obj.strides)
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            ae(c[i, j], c_obj[i, j])

    ae(tuple([d.shape[i] for i in range(2)]), d_obj.shape)
    ae(tuple([d.strides[i] for i in range(2)]), d_obj.strides)
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ae(d[i, j], d_obj[i, j])

    e = a[..., 5, 6]
    e_obj = array[..., 5, 6]
    ae(e.shape[0], e_obj.shape[0])
    ae(e.strides[0], e_obj.strides[0])

@testcase
def test_transpose():
    """
    >>> test_transpose()
    3 4
    (3, 4)
    (3, 4)
    11 11 11 11 11 11
    """
    cdef dtype_t[:, :] a

    numpy_obj = np.arange(4 * 3, dtype=np.int32).reshape(4, 3)

    a = numpy_obj
    a_obj = a

    cdef dtype_t[:, :] b = a.T
    print a.T.shape[0], a.T.shape[1]
    print a_obj.T.shape
    print numpy_obj.T.shape

    cdef dtype_t[:, :] c
    with nogil:
        c = a.T.T

    assert (<object> a).shape == (<object> c).shape
    assert (<object> a).strides == (<object> c).strides

    print a[3, 2], a.T[2, 3], a_obj[3, 2], a_obj.T[2, 3], numpy_obj[3, 2], numpy_obj.T[2, 3]

@testcase_numpy_1_5
def test_numpy_like_attributes(cyarray):
    """
    For some reason this fails in numpy 1.4, with shape () and strides (40, 8)
    instead of 20, 4 on my machine. Investigate this.

    >>> cyarray = create_array(shape=(8, 5), mode="c")
    >>> test_numpy_like_attributes(cyarray)
    >>> test_numpy_like_attributes(cyarray.memview)
    """
    numarray = np.asarray(cyarray)

    assert cyarray.shape == numarray.shape, (cyarray.shape, numarray.shape)
    assert cyarray.strides == numarray.strides, (cyarray.strides, numarray.strides)
    assert cyarray.ndim == numarray.ndim, (cyarray.ndim, numarray.ndim)
    assert cyarray.size == numarray.size, (cyarray.size, numarray.size)
    assert cyarray.nbytes == numarray.nbytes, (cyarray.nbytes, numarray.nbytes)

    cdef int[:, :] mslice = numarray
    assert (<object> mslice).base is numarray

@testcase_numpy_1_5
def test_copy_and_contig_attributes(a):
    """
    >>> a = np.arange(20, dtype=np.int32).reshape(5, 4)
    >>> test_copy_and_contig_attributes(a)
    """
    cdef np.int32_t[:, :] mslice = a
    m = mslice

    # Test object copy attributes
    assert np.all(a == np.array(m.copy()))
    assert a.strides == m.strides == m.copy().strides

    assert np.all(a == np.array(m.copy_fortran()))
    assert m.copy_fortran().strides == (4, 20)

    # Test object is_*_contig attributes
    assert m.is_c_contig() and m.copy().is_c_contig()
    assert m.copy_fortran().is_f_contig() and not m.is_f_contig()

ctypedef int td_cy_int
cdef extern from "bufaccess.h":
    ctypedef td_cy_int td_h_short # Defined as short, but Cython doesn't know this!
    ctypedef float td_h_double # Defined as double
    ctypedef unsigned int td_h_ushort # Defined as unsigned short
ctypedef td_h_short td_h_cy_short

cdef void dealloc_callback(void *data):
    print "deallocating..."

def build_numarray(array array):
    array.callback_free_data = dealloc_callback
    return np.asarray(array)

def index(array array):
    print build_numarray(array)[3, 2]

@testcase_numpy_1_5
def test_coerce_to_numpy():
    """
    Test coercion to NumPy arrays, especially with automatically
    generated format strings.

    >>> test_coerce_to_numpy()
    [97, 98, 600, 700, 800]
    deallocating...
    (600, 700)
    deallocating...
    ((100, 200), (300, 400), 500)
    deallocating...
    (97, 900)
    deallocating...
    99
    deallocating...
    111
    deallocating...
    222
    deallocating...
    333
    deallocating...
    11.1
    deallocating...
    12.2
    deallocating...
    13.3
    deallocating...
    (14.4+15.5j)
    deallocating...
    (16.6+17.7j)
    deallocating...
    (18.8+19.9j)
    deallocating...
    22
    deallocating...
    33.33
    deallocating...
    44
    deallocating...
    """
    #
    ### First set up some C arrays that will be used to hold data
    #
    cdef MyStruct mystructs[20]
    cdef SmallStruct smallstructs[20]
    cdef NestedStruct nestedstructs[20]
    cdef PackedStruct packedstructs[20]

    cdef char chars[20]
    cdef short shorts[20]
    cdef int ints[20]
    cdef long long longlongs[20]
    cdef td_h_short externs[20]

    cdef float floats[20]
    cdef double doubles[20]
    cdef long double longdoubles[20]

    cdef float complex floatcomplex[20]
    cdef double complex doublecomplex[20]
    cdef long double complex longdoublecomplex[20]

    cdef td_h_short h_shorts[20]
    cdef td_h_double h_doubles[20]
    cdef td_h_ushort h_ushorts[20]

    cdef Py_ssize_t idx = 17

    #
    ### Initialize one element in each array
    #
    mystructs[idx] = {
        'a': 'a',
        'b': 'b',
        'c': 600,
        'd': 700,
        'e': 800,
    }

    smallstructs[idx] = { 'a': 600, 'b': 700 }

    nestedstructs[idx] = {
        'x': { 'a': 100, 'b': 200 },
        'y': { 'a': 300, 'b': 400 },
        'z': 500,
    }

    packedstructs[idx] = { 'a': 'a', 'b': 900 }

    chars[idx] = 99
    shorts[idx] = 111
    ints[idx] = 222
    longlongs[idx] = 333
    externs[idx] = 444

    floats[idx] = 11.1
    doubles[idx] = 12.2
    longdoubles[idx] = 13.3

    floatcomplex[idx] = 14.4 + 15.5j
    doublecomplex[idx] = 16.6 + 17.7j
    longdoublecomplex[idx] = 18.8 + 19.9j

    h_shorts[idx] = 22
    h_doubles[idx] = 33.33
    h_ushorts[idx] = 44

    #
    ### Create a NumPy array and see if our element can be correctly retrieved
    #
    mystruct_array = build_numarray(<MyStruct[:4, :5]> <MyStruct *> mystructs)
    print [int(x) for x in mystruct_array[3, 2]]
    del mystruct_array
    index(<SmallStruct[:4, :5]> <SmallStruct *> smallstructs)
    index(<NestedStruct[:4, :5]> <NestedStruct *> nestedstructs)
    index(<PackedStruct[:4, :5]> <PackedStruct *> packedstructs)

    index(<char[:4, :5]> <char *> chars)
    index(<short[:4, :5]> <short *> shorts)
    index(<int[:4, :5]> <int *> ints)
    index(<long long[:4, :5]> <long long *> longlongs)

    index(<float[:4, :5]> <float *> floats)
    index(<double[:4, :5]> <double *> doubles)
    index(<long double[:4, :5]> <long double *> longdoubles)

    index(<float complex[:4, :5]> <float complex *> floatcomplex)
    index(<double complex[:4, :5]> <double complex *> doublecomplex)
    index(<long double complex[:4, :5]> <long double complex *> longdoublecomplex)

    index(<td_h_short[:4, :5]> <td_h_short *> h_shorts)
    index(<td_h_double[:4, :5]> <td_h_double *> h_doubles)
    index(<td_h_ushort[:4, :5]> <td_h_ushort *> h_ushorts)


@testcase_numpy_1_5
def test_memslice_getbuffer():
    """
    >>> test_memslice_getbuffer()
    [[ 0  2  4]
     [10 12 14]]
    callback called
    """
    cdef int[:, :] array = create_array((4, 5), mode="c", use_callback=True)
    print np.asarray(array)[::2, ::2]

cdef class DeallocateMe(object):
    def __dealloc__(self):
        print "deallocated!"

# Disabled! References cycles don't seem to be supported by NumPy
# @testcase
def acquire_release_cycle(obj):
    """
    >>> a = np.arange(20, dtype=np.object)
    >>> a[10] = DeallocateMe()
    >>> acquire_release_cycle(a)
    deallocated!
    """
    import gc

    cdef object[:] buf = obj
    buf[1] = buf

    gc.collect()

    del buf

    gc.collect()

cdef packed struct StructArray:
    int a[4]
    char b[5]

@testcase_numpy_1_5
def test_memslice_structarray(data, dtype):
    """
    >>> def b(s): return s.encode('ascii')
    >>> def to_byte_values(b):
    ...     if sys.version_info[0] >= 3: return list(b)
    ...     else: return map(ord, b)

    >>> data = [(range(4), b('spam\\0')), (range(4, 8), b('ham\\0\\0')), (range(8, 12), b('eggs\\0'))]
    >>> dtype = np.dtype([('a', '4i'), ('b', '5b')])
    >>> test_memslice_structarray([(L, to_byte_values(s)) for L, s in data], dtype)
    0
    1
    2
    3
    spam
    4
    5
    6
    7
    ham
    8
    9
    10
    11
    eggs

    Test the same thing with the string format specifier

    >>> dtype = np.dtype([('a', '4i'), ('b', 'S5')])
    >>> test_memslice_structarray(data, dtype)
    0
    1
    2
    3
    spam
    4
    5
    6
    7
    ham
    8
    9
    10
    11
    eggs
    """
    a = np.empty((3,), dtype=dtype)
    a[:] = data
    cdef StructArray[:] myslice = a
    cdef int i, j
    for i in range(3):
        for j in range(4):
            print myslice[i].a[j]
        print myslice[i].b.decode('ASCII')

@testcase_numpy_1_5
def test_structarray_errors(StructArray[:] a):
    """
    >>> dtype = np.dtype([('a', '4i'), ('b', '5b')])
    >>> test_structarray_errors(np.empty((5,), dtype=dtype))

    >>> dtype = np.dtype([('a', '6i'), ('b', '5b')])
    >>> test_structarray_errors(np.empty((5,), dtype=dtype))
    Traceback (most recent call last):
       ...
    ValueError: Expected a dimension of size 4, got 6

    >>> dtype = np.dtype([('a', '(4,4)i'), ('b', '5b')])
    >>> test_structarray_errors(np.empty((5,), dtype=dtype))
    Traceback (most recent call last):
       ...
    ValueError: Expected 1 dimension(s), got 2

    Test the same thing with the string format specifier

    >>> dtype = np.dtype([('a', '4i'), ('b', 'S5')])
    >>> test_structarray_errors(np.empty((5,), dtype=dtype))

    >>> dtype = np.dtype([('a', '6i'), ('b', 'S5')])
    >>> test_structarray_errors(np.empty((5,), dtype=dtype))
    Traceback (most recent call last):
       ...
    ValueError: Expected a dimension of size 4, got 6

    >>> dtype = np.dtype([('a', '(4,4)i'), ('b', 'S5')])
    >>> test_structarray_errors(np.empty((5,), dtype=dtype))
    Traceback (most recent call last):
       ...
    ValueError: Expected 1 dimension(s), got 2
    """

cdef struct StringStruct:
    char c[4][4]

ctypedef char String[4][4]

def stringstructtest(StringStruct[:] view):
    pass

def stringtest(String[:] view):
    pass

@testcase_numpy_1_5
def test_string_invalid_dims():
    """
    >>> def b(s): return s.encode('ascii')
    >>> dtype = np.dtype([('a', 'S4')])
    >>> data = [b('spam'), b('eggs')]
    >>> stringstructtest(np.array(data, dtype=dtype))
    Traceback (most recent call last):
       ...
    ValueError: Expected 2 dimensions, got 1
    >>> stringtest(np.array(data, dtype='S4'))
    Traceback (most recent call last):
       ...
    ValueError: Expected 2 dimensions, got 1
    """

ctypedef struct AttributesStruct:
    int attrib1
    float attrib2
    StringStruct attrib3

@testcase_numpy_1_5
def test_struct_attributes():
    """
    >>> test_struct_attributes()
    1
    2.0
    c
    """
    cdef AttributesStruct[10] a
    cdef AttributesStruct[:] myslice = a
    myslice[0].attrib1 = 1
    myslice[0].attrib2 = 2.0
    myslice[0].attrib3.c[0][0] = 'c'

    array = np.asarray(myslice)
    print array[0]['attrib1']
    print array[0]['attrib2']
    print chr(array[0]['attrib3']['c'][0][0])
