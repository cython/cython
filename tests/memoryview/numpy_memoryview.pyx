# tag: numpy
# mode: run

"""
Test slicing for memoryviews and memoryviewslices
"""

import sys

cimport numpy as np
import numpy as np
cimport cython
from cython cimport view

include "../testsupport/cythonarrayutil.pxi"
include "../buffers/mockbuffers.pxi"

ctypedef np.int32_t dtype_t

IS_PYPY = hasattr(sys, 'pypy_version_info')
NUMPY_VERSION = tuple(int(v) for v in np.__version__.split('.')[:2])
print(NUMPY_VERSION)

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

def testcase_no_pypy(f, _is_pypy=hasattr(sys, "pypy_version_info")):
    if _is_pypy:
        f.__doc__ = ""  # disable the tests
    return f

def gc_collect_if_required():
    if NUMPY_VERSION >= (1, 14) or IS_PYPY:
        import gc
        gc.collect()


#
### Test slicing memoryview slices
#

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
    cdef object a_obj = a

    cdef dtype_t[:, :] b = a.T
    print a.T.shape[0], a.T.shape[1]
    print a_obj.T.shape
    print tuple(map(int, numpy_obj.T.shape)) # might use longs in Py2

    cdef dtype_t[:, :] c
    with nogil:
        c = a.T.T

    assert (<object> a).shape == (<object> c).shape
    assert (<object> a).strides == (<object> c).strides

    print a[3, 2], a.T[2, 3], a_obj[3, 2], a_obj.T[2, 3], numpy_obj[3, 2], numpy_obj.T[2, 3]


def test_transpose_type(a):
    """
    >>> a = np.zeros((5, 10), dtype=np.float64)
    >>> a[4, 6] = 9
    >>> test_transpose_type(a)
    9.0
    """
    cdef double[:, ::1] m = a
    cdef double[::1, :] m_transpose = a.T
    print m_transpose[6, 4]


def test_numpy_like_attributes(cyarray):
    """
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

def test_copy_and_contig_attributes(a):
    """
    >>> a = np.arange(20, dtype=np.int32).reshape(5, 4)
    >>> test_copy_and_contig_attributes(a)
    """
    cdef np.int32_t[:, :] mslice = a
    cdef object m = mslice  #  object copy

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

cdef void dealloc_callback(void *data) noexcept:
    print "deallocating..."

def build_numarray(array array):
    array.callback_free_data = dealloc_callback
    return np.asarray(array)

def index(array array):
    print build_numarray(array)[3, 2]

@testcase_no_pypy
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
    13.25
    deallocating...
    (14.4+15.5j)
    deallocating...
    (16.5+17.7j)
    deallocating...
    (18.8125+19.9375j)
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
    cdef MyStruct[20] mystructs
    cdef SmallStruct[20] smallstructs
    cdef NestedStruct[20] nestedstructs
    cdef PackedStruct[20] packedstructs

    cdef signed char[20] chars
    cdef short[20] shorts
    cdef int[20] ints
    cdef long long[20] longlongs
    cdef td_h_short[20] externs

    cdef float[20] floats
    cdef double[20] doubles
    cdef long double[20] longdoubles

    cdef float complex[20] floatcomplex
    cdef double complex[20] doublecomplex
    cdef long double complex[20] longdoublecomplex

    cdef td_h_short[20] h_shorts
    cdef td_h_double[20] h_doubles
    cdef td_h_ushort[20] h_ushorts

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
    assert externs[idx] == 444  # avoid "set but not used" C compiler warning

    floats[idx] = 11.1
    doubles[idx] = 12.2
    longdoubles[idx] = 13.25

    floatcomplex[idx] = 14.4 + 15.5j
    doublecomplex[idx] = 16.5 + 17.7j
    longdoublecomplex[idx] = 18.8125 + 19.9375j  # x/64 to avoid float format rounding issues

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

    index(<signed char[:4, :5]> <signed char *> chars)
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


@testcase_no_pypy
def test_memslice_getbuffer():
    """
    >>> test_memslice_getbuffer(); gc_collect_if_required()
    [[ 0  2  4]
     [10 12 14]]
    callback called
    """
    cdef int[:, :] array = create_array((4, 5), mode="c", use_callback=True)
    print(np.asarray(array)[::2, ::2])

cdef class DeallocateMe(object):
    def __dealloc__(self):
        print "deallocated!"

# Disabled! References cycles don't seem to be supported by NumPy
# @testcase
def acquire_release_cycle(obj):
    DISABLED_DOCSTRING = """
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
    signed char b[5]

def test_memslice_structarray(data, dtype):
    """
    >>> def b(s): return s.encode('ascii')
    >>> def to_byte_values(b): return list(b)

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
    signed char c[4][4]

ctypedef signed char String[4][4]

def stringstructtest(StringStruct[:] view):
    pass

def stringtest(String[:] view):
    pass

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

#
### Test for NULL strides (C contiguous buffers)
#
cdef getbuffer(Buffer self, Py_buffer *info):
    info.buf = &self.m[0, 0]
    info.len = 10 * 20
    info.ndim = 2
    info.shape = self._shape
    info.strides = NULL
    info.suboffsets = NULL
    info.itemsize = 4
    info.readonly = 0
    self.format = b"f"
    info.format = self.format

cdef class Buffer(object):
    cdef Py_ssize_t[2] _shape
    cdef bytes format
    cdef float[:, :] m
    cdef object shape, strides

    def __init__(self):
        a = np.arange(200, dtype=np.float32).reshape(10, 20)
        self.m = a
        self.shape = a.shape
        self.strides = a.strides
        self._shape[0] = 10
        self._shape[1] = 20

    def __getbuffer__(self, Py_buffer *info, int flags):
        getbuffer(self, info)

cdef class SuboffsetsNoStridesBuffer(Buffer):
    def __getbuffer__(self, Py_buffer *info, int flags):
        getbuffer(self, info)
        info.suboffsets = self._shape

def test_null_strides(Buffer buffer_obj):
    """
    >>> test_null_strides(Buffer())
    """
    cdef float[:, :] m1 = buffer_obj
    cdef float[:, ::1] m2 = buffer_obj
    cdef float[:, ::view.contiguous] m3 = buffer_obj

    assert (<object> m1).strides == buffer_obj.strides
    assert (<object> m2).strides == buffer_obj.strides, ((<object> m2).strides, buffer_obj.strides)
    assert (<object> m3).strides == buffer_obj.strides

    cdef int i, j
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            assert m1[i, j] == buffer_obj.m[i, j]
            assert m2[i, j] == buffer_obj.m[i, j], (i, j, m2[i, j], buffer_obj.m[i, j])
            assert m3[i, j] == buffer_obj.m[i, j]

def test_null_strides_error(buffer_obj):
    """
    >>> test_null_strides_error(Buffer())
    C-contiguous buffer is not indirect in dimension 1
    C-contiguous buffer is not indirect in dimension 0
    C-contiguous buffer is not contiguous in dimension 0
    C-contiguous buffer is not contiguous in dimension 0
    >>> test_null_strides_error(SuboffsetsNoStridesBuffer())
    Traceback (most recent call last):
        ...
    ValueError: Buffer exposes suboffsets but no strides
    """
    # valid
    cdef float[::view.generic, ::view.generic] full_buf = buffer_obj

    # invalid
    cdef float[:, ::view.indirect] indirect_buf1
    cdef float[::view.indirect, :] indirect_buf2
    cdef float[::1, :] fortran_buf1
    cdef float[::view.contiguous, :] fortran_buf2

    try:
        indirect_buf1 = buffer_obj
    except ValueError, e:
        print e

    try:
        indirect_buf2 = buffer_obj
    except ValueError, e:
        print e

    try:
        fortran_buf1 = buffer_obj
    except ValueError, e:
        print e

    try:
        fortran_buf2 = buffer_obj
    except ValueError, e:
        print e

def test_refcount_GH507():
    """
    >>> test_refcount_GH507()
    """
    a = np.arange(12, dtype='int32').reshape([3, 4])
    cdef np.int32_t[:,:] a_view = a
    cdef np.int32_t[:,:] b = a_view[1:2,:].T


@cython.boundscheck(False)
@cython.wraparound(False)
def test_boundscheck_and_wraparound(double[:, :] x):
    """
    >>> import numpy as np
    >>> array = np.ones((2,2)) * 3.5
    >>> test_boundscheck_and_wraparound(array)
    """
    # Make sure we don't generate C compiler warnings for unused code here.
    cdef Py_ssize_t numrow = x.shape[0]
    cdef Py_ssize_t i
    for i in range(numrow):
        x[i, 0]
        x[i]
        x[i, ...]
        x[i, :]


ctypedef struct SameTypeAfterArraysStructSimple:
    double a[16]
    double b[16]
    double c

def same_type_after_arrays_simple():
    """
    >>> same_type_after_arrays_simple()
    """

    cdef SameTypeAfterArraysStructSimple element
    arr = np.ones(2, np.asarray(<SameTypeAfterArraysStructSimple[:1]>&element).dtype)
    cdef SameTypeAfterArraysStructSimple[:] memview = arr


ctypedef struct SameTypeAfterArraysStructComposite:
    int a
    float b[8]
    float c
    unsigned long d
    int e[5]
    int f
    int g
    double h[4]
    int i

def same_type_after_arrays_composite():
    """
    >>> same_type_after_arrays_composite()
    """

    cdef SameTypeAfterArraysStructComposite element
    arr = np.ones(2, np.asarray(<SameTypeAfterArraysStructComposite[:1]>&element).dtype)
    cdef SameTypeAfterArraysStructComposite[:] memview = arr

ctypedef fused np_numeric_t:
    np.float64_t

def test_invalid_buffer_fused_memoryview(np_numeric_t[:] A):
    """
    >>> import numpy as np
    >>> zz = np.zeros([5], dtype='M')
    >>> test_invalid_buffer_fused_memoryview(zz)
    Traceback (most recent call last):
        ...
    TypeError: No matching signature found
    """
    return

ctypedef fused np_numeric_object_t:
    np.float64_t[:]
    object

def test_valid_buffer_fused_memoryview(np_numeric_object_t A):
    """
    >>> import numpy as np
    >>> zz = np.zeros([5], dtype='M')
    >>> test_valid_buffer_fused_memoryview(zz)
    """
    return
