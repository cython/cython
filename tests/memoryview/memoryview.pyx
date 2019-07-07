# mode: run

u'''
>>> f()
>>> g()
>>> call()
>>> assignmvs()
'''

from cython.view cimport memoryview, array
from cython cimport view

from cpython.object cimport PyObject
from cpython.ref cimport Py_INCREF, Py_DECREF
cimport cython

import array as pyarray
from libc.stdlib cimport malloc, free

cdef extern from "Python.h":
    cdef int PyBUF_C_CONTIGUOUS

include "../buffers/mockbuffers.pxi"

#
### Test for some coercions
#
def init_obj():
    return 3

cdef passmvs(float[:,::1] mvs, object foo):
    mvs = array((10,10), itemsize=sizeof(float), format='f')
    foo = init_obj()

cdef object returnobj():
    cdef obj = object()
    return obj

cdef float[::1] returnmvs_inner():
    return array((10,), itemsize=sizeof(float), format='f')

cdef float[::1] returnmvs():
    cdef float[::1] mvs = returnmvs_inner()
    return mvs

def f():
    cdef array arr = array(shape=(10,10), itemsize=sizeof(int), format='i')
    cdef memoryview mv = memoryview(arr, PyBUF_C_CONTIGUOUS)

def g():
    cdef object obj = init_obj()
    cdef int[::1] mview = array((10,), itemsize=sizeof(int), format='i')
    obj = init_obj()
    mview = array((10,), itemsize=sizeof(int), format='i')

cdef class ExtClass(object):
    cdef int[::1] mview

    def __init__(self):
        self.mview = array((10,), itemsize=sizeof(int), format='i')
        self.mview = array((10,), itemsize=sizeof(int), format='i')

class PyClass(object):

    def __init__(self):
        self.mview = array((10,), itemsize=sizeof(long), format='l')

cdef cdg():
    cdef double[::1] dmv = array((10,), itemsize=sizeof(double), format='d')
    dmv = array((10,), itemsize=sizeof(double), format='d')

cdef class TestExcClassExternalDtype(object):
    cdef ext_dtype[:, :] arr_float
    cdef td_h_double[:, :] arr_double

    def __init__(self):
        self.arr_float = array((10, 10), itemsize=sizeof(ext_dtype), format='f')
        self.arr_float[:] = 0.0
        self.arr_float[4, 4] = 2.0

        self.arr_double = array((10, 10), itemsize=sizeof(td_h_double), format='d')
        self.arr_double[:] = 0.0
        self.arr_double[4, 4] = 2.0

def test_external_dtype():
    """
    >>> test_external_dtype()
    2.0
    2.0
    """
    cdef TestExcClassExternalDtype obj = TestExcClassExternalDtype()
    print obj.arr_float[4, 4]
    print obj.arr_double[4, 4]


cdef class ExtClassMockedAttr(object):
    cdef int[:, :] arr

    def __init__(self):
        self.arr = IntMockBuffer("self.arr", range(100), (10, 8))
        self.arr[:] = 0
        self.arr[4, 4] = 2

cdef int[:, :] _coerce_to_temp():
    cdef ExtClassMockedAttr obj = ExtClassMockedAttr()
    return obj.arr

def test_coerce_to_temp():
    """
    >>> test_coerce_to_temp()
    acquired self.arr
    released self.arr
    <BLANKLINE>
    acquired self.arr
    released self.arr
    <BLANKLINE>
    acquired self.arr
    released self.arr
    2
    <BLANKLINE>
    acquired self.arr
    released self.arr
    2
    <BLANKLINE>
    acquired self.arr
    released self.arr
    2
    """
    _coerce_to_temp()[:] = 0
    print
    _coerce_to_temp()[...] = 0
    print
    print _coerce_to_temp()[4, 4]
    print
    print _coerce_to_temp()[..., 4][4]
    print
    print _coerce_to_temp()[4][4]

def test_extclass_attribute_dealloc():
    """
    >>> test_extclass_attribute_dealloc()
    acquired self.arr
    2
    released self.arr
    """
    cdef ExtClassMockedAttr obj = ExtClassMockedAttr()
    print obj.arr[4, 4]

cdef float[:,::1] global_mv = array((10,10), itemsize=sizeof(float), format='f')
global_mv = array((10,10), itemsize=sizeof(float), format='f')
cdef object global_obj

def assignmvs():
    cdef int[::1] mv1, mv2
    cdef int[:] mv3
    mv1 = array((10,), itemsize=sizeof(int), format='i')
    mv2 = mv1
    mv1 = mv2
    mv3 = mv2

def call():
    global global_mv
    passmvs(global_mv, global_obj)
    global_mv = array((3,3), itemsize=sizeof(float), format='f')
    cdef float[::1] getmvs = returnmvs()
    returnmvs()
    cdef object obj = returnobj()
    cdg()
    f = ExtClass()
    pf = PyClass()

cdef ExtClass get_ext_obj():
    print 'get_ext_obj called'
    return ExtClass.__new__(ExtClass)

def test_cdef_attribute():
    """
    >>> test_cdef_attribute()
    Memoryview is not initialized
    local variable 'myview' referenced before assignment
    local variable 'myview' referenced before assignment
    get_ext_obj called
    Memoryview is not initialized
    <MemoryView of 'array' object>
    """
    cdef ExtClass extobj = ExtClass.__new__(ExtClass)
    try:
        print extobj.mview
    except AttributeError, e:
        print e.args[0]
    else:
        print "No AttributeError was raised"

    cdef int[:] myview
    try:
        print myview
    except UnboundLocalError, e:
        print e.args[0]
    else:
        print "No UnboundLocalError was raised"

    cdef int[:] otherview
    try:
         otherview = myview
    except UnboundLocalError, e:
        print e.args[0]

    try:
        print get_ext_obj().mview
    except AttributeError, e:
        print e.args[0]
    else:
        print "No AttributeError was raised"

    print ExtClass().mview

@cython.boundscheck(False)
def test_nogil_unbound_localerror():
    """
    >>> test_nogil_unbound_localerror()
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'm' referenced before assignment
    """
    cdef int[:] m
    with nogil:
        m[0] = 10

def test_nogil_oob():
    """
    >>> test_nogil_oob()
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    """
    cdef int[5] a
    cdef int[:] m = a
    with nogil:
        m[5] = 1

def basic_struct(MyStruct[:] mslice):
    """
    See also buffmt.pyx

    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="ccqii"))
    [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
    """
    buf = mslice
    print sorted([(k, int(v)) for k, v in buf[0].items()])

def nested_struct(NestedStruct[:] mslice):
    """
    See also buffmt.pyx

    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="T{ii}T{2i}i"))
    1 2 3 4 5
    """
    buf = mslice
    d = buf[0]
    print d['x']['a'], d['x']['b'], d['y']['a'], d['y']['b'], d['z']

def packed_struct(PackedStruct[:] mslice):
    """
    See also buffmt.pyx

    >>> packed_struct(PackedStructMockBuffer(None, [(1, 2)]))
    1 2
    >>> packed_struct(PackedStructMockBuffer(None, [(1, 2)], format="T{c^i}"))
    1 2
    >>> packed_struct(PackedStructMockBuffer(None, [(1, 2)], format="T{c=i}"))
    1 2

    """
    buf = mslice
    print buf[0]['a'], buf[0]['b']

def nested_packed_struct(NestedPackedStruct[:] mslice):
    """
    See also buffmt.pyx

    >>> nested_packed_struct(NestedPackedStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> nested_packed_struct(NestedPackedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="ci^ci@i"))
    1 2 3 4 5
    >>> nested_packed_struct(NestedPackedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="^c@i^ci@i"))
    1 2 3 4 5
    """
    buf = mslice
    d = buf[0]
    print d['a'], d['b'], d['sub']['a'], d['sub']['b'], d['c']


def complex_dtype(long double complex[:] mslice):
    """
    >>> complex_dtype(LongComplexMockBuffer(None, [(0, -1)]))
    -1j
    """
    buf = mslice
    print buf[0]

def complex_inplace(long double complex[:] mslice):
    """
    >>> complex_inplace(LongComplexMockBuffer(None, [(0, -1)]))
    (1+1j)
    """
    buf = mslice
    buf[0] = buf[0] + 1 + 2j
    print buf[0]

def complex_struct_dtype(LongComplex[:] mslice):
    """
    Note that the format string is "Zg" rather than "2g", yet a struct
    is accessed.
    >>> complex_struct_dtype(LongComplexMockBuffer(None, [(0, -1)]))
    0.0 -1.0
    """
    buf = mslice
    print buf[0]['real'], buf[0]['imag']

#
# Getting items and index bounds checking
#
def get_int_2d(int[:, :] mslice, int i, int j):
    """
    >>> C = IntMockBuffer("C", range(6), (2,3))
    >>> get_int_2d(C, 1, 1)
    acquired C
    released C
    4

    Check negative indexing:
    >>> get_int_2d(C, -1, 0)
    acquired C
    released C
    3
    >>> get_int_2d(C, -1, -2)
    acquired C
    released C
    4
    >>> get_int_2d(C, -2, -3)
    acquired C
    released C
    0

    Out-of-bounds errors:
    >>> get_int_2d(C, 2, 0)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    >>> get_int_2d(C, 0, -4)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 1)
    """
    buf = mslice
    return buf[i, j]

def set_int_2d(int[:, :] mslice, int i, int j, int value):
    """
    Uses get_int_2d to read back the value afterwards. For pure
    unit test, one should support reading in MockBuffer instead.

    >>> C = IntMockBuffer("C", range(6), (2,3))
    >>> set_int_2d(C, 1, 1, 10)
    acquired C
    released C
    >>> get_int_2d(C, 1, 1)
    acquired C
    released C
    10

    Check negative indexing:
    >>> set_int_2d(C, -1, 0, 3)
    acquired C
    released C
    >>> get_int_2d(C, -1, 0)
    acquired C
    released C
    3

    >>> set_int_2d(C, -1, -2, 8)
    acquired C
    released C
    >>> get_int_2d(C, -1, -2)
    acquired C
    released C
    8

    >>> set_int_2d(C, -2, -3, 9)
    acquired C
    released C
    >>> get_int_2d(C, -2, -3)
    acquired C
    released C
    9

    Out-of-bounds errors:
    >>> set_int_2d(C, 2, 0, 19)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    >>> set_int_2d(C, 0, -4, 19)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 1)

    """
    buf = mslice
    buf[i, j] = value


#
# Test all kinds of indexing and flags
#

def writable(unsigned short int[:, :, :] mslice):
    """
    >>> R = UnsignedShortMockBuffer("R", range(27), shape=(3, 3, 3))
    >>> writable(R)
    acquired R
    released R
    >>> [str(x) for x in R.received_flags] # Py2/3
    ['FORMAT', 'ND', 'STRIDES', 'WRITABLE']
    """
    buf = mslice
    buf[2, 2, 1] = 23

def strided(int[:] mslice):
    """
    >>> A = IntMockBuffer("A", range(4))
    >>> strided(A)
    acquired A
    released A
    2

    Check that the suboffsets were patched back prior to release.
    >>> A.release_ok
    True
    """
    buf = mslice
    return buf[2]

def c_contig(int[::1] mslice):
    """
    >>> A = IntMockBuffer(None, range(4))
    >>> c_contig(A)
    2
    """
    buf = mslice
    return buf[2]

def c_contig_2d(int[:, ::1] mslice):
    """
    Multi-dim has separate implementation

    >>> A = IntMockBuffer(None, range(12), shape=(3,4))
    >>> c_contig_2d(A)
    7
    """
    buf = mslice
    return buf[1, 3]

def f_contig(int[::1, :] mslice):
    """
    >>> A = IntMockBuffer(None, range(4), shape=(2, 2), strides=(1, 2))
    >>> f_contig(A)
    2
    """
    buf = mslice
    return buf[0, 1]

def f_contig_2d(int[::1, :] mslice):
    """
    Must set up strides manually to ensure Fortran ordering.

    >>> A = IntMockBuffer(None, range(12), shape=(4,3), strides=(1, 4))
    >>> f_contig_2d(A)
    7
    """
    buf = mslice
    return buf[3, 1]

def generic(int[::view.generic, ::view.generic] mslice1,
            int[::view.generic, ::view.generic] mslice2):
    """
    >>> A = IntMockBuffer("A", [[0,1,2], [3,4,5], [6,7,8]])
    >>> B = IntMockBuffer("B", [[0,1,2], [3,4,5], [6,7,8]], shape=(3, 3), strides=(1, 3))
    >>> generic(A, B)
    acquired A
    acquired B
    4
    4
    10
    11
    released A
    released B
    """
    buf1, buf2 = mslice1, mslice2

    print buf1[1, 1]
    print buf2[1, 1]

    buf1[2, -1] = 10
    buf2[2, -1] = 11

    print buf1[2, 2]
    print buf2[2, 2]

#def generic_contig(int[::view.generic_contiguous, :] mslice1,
#                   int[::view.generic_contiguous, :] mslice2):
#    """
#    >>> A = IntMockBuffer("A", [[0,1,2], [3,4,5], [6,7,8]])
#    >>> B = IntMockBuffer("B", [[0,1,2], [3,4,5], [6,7,8]], shape=(3, 3), strides=(1, 3))
#    >>> generic_contig(A, B)
#    acquired A
#    acquired B
#    4
#    4
#    10
#    11
#    released A
#    released B
#    """
#    buf1, buf2 = mslice1, mslice2
#
#    print buf1[1, 1]
#    print buf2[1, 1]
#
#    buf1[2, -1] = 10
#    buf2[2, -1] = 11
#
#    print buf1[2, 2]
#    print buf2[2, 2]

ctypedef int td_cy_int
cdef extern from "bufaccess.h":
    ctypedef td_cy_int td_h_short # Defined as short, but Cython doesn't know this!
    ctypedef float td_h_double # Defined as double
    ctypedef unsigned int td_h_ushort # Defined as unsigned short
ctypedef td_h_short td_h_cy_short

def printbuf_td_cy_int(td_cy_int[:] mslice, shape):
    """
    >>> printbuf_td_cy_int(IntMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_cy_int(ShortMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_cy_int' but got 'short'
    """
    buf = mslice
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

def printbuf_td_h_short(td_h_short[:] mslice, shape):
    """
    >>> printbuf_td_h_short(ShortMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_h_short(IntMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_short' but got 'int'
    """
    buf = mslice
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

def printbuf_td_h_cy_short(td_h_cy_short[:] mslice, shape):
    """
    >>> printbuf_td_h_cy_short(ShortMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_h_cy_short(IntMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_cy_short' but got 'int'
    """
    buf = mslice
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

def printbuf_td_h_ushort(td_h_ushort[:] mslice, shape):
    """
    >>> printbuf_td_h_ushort(UnsignedShortMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_h_ushort(ShortMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_ushort' but got 'short'
    """
    buf = mslice
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

def printbuf_td_h_double(td_h_double[:] mslice, shape):
    """
    >>> printbuf_td_h_double(DoubleMockBuffer(None, [0.25, 1, 3.125]), (3,))
    0.25 1.0 3.125 END
    >>> printbuf_td_h_double(FloatMockBuffer(None, [0.25, 1, 3.125]), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_double' but got 'float'
    """
    buf = mslice
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

#
# Object access
#
def addref(*args):
    for item in args: Py_INCREF(item)
def decref(*args):
    for item in args: Py_DECREF(item)

def get_refcount(x):
    return (<PyObject*>x).ob_refcnt

def printbuf_object(object[:] mslice, shape):
    """
    Only play with unique objects, interned numbers etc. will have
    unpredictable refcounts.

    ObjectMockBuffer doesn't do anything about increfing/decrefing,
    we to the "buffer implementor" refcounting directly in the
    testcase.

    >>> a, b, c = "globally_unique_string_23234123", {4:23}, [34,3]
    >>> get_refcount(a), get_refcount(b), get_refcount(c)
    (2, 2, 2)
    >>> A = ObjectMockBuffer(None, [a, b, c])
    >>> printbuf_object(A, (3,))
    'globally_unique_string_23234123' 2
    {4: 23} 2
    [34, 3] 2
    """
    buf = mslice
    cdef int i
    for i in range(shape[0]):
        print repr(buf[i]), (<PyObject*>buf[i]).ob_refcnt

def assign_to_object(object[:] mslice, int idx, obj):
    """
    See comments on printbuf_object above.

    >>> a, b = [1, 2, 3], [4, 5, 6]
    >>> get_refcount(a), get_refcount(b)
    (2, 2)
    >>> addref(a)
    >>> A = ObjectMockBuffer(None, [1, a]) # 1, ...,otherwise it thinks nested lists...
    >>> get_refcount(a), get_refcount(b)
    (3, 2)
    >>> assign_to_object(A, 1, b)
    >>> get_refcount(a), get_refcount(b)
    (2, 3)
    >>> decref(b)
    """
    buf = mslice
    buf[idx] = obj

def assign_temporary_to_object(object[:] mslice):
    """
    See comments on printbuf_object above.

    >>> a, b = [1, 2, 3], {4:23}
    >>> get_refcount(a)
    2
    >>> addref(a)
    >>> A = ObjectMockBuffer(None, [b, a])
    >>> get_refcount(a)
    3
    >>> assign_temporary_to_object(A)
    >>> get_refcount(a)
    2

    >>> printbuf_object(A, (2,))
    {4: 23} 2
    {1: 8} 2

    To avoid leaking a reference in our testcase we need to
    replace the temporary with something we can manually decref :-)
    >>> assign_to_object(A, 1, a)
    >>> decref(a)
    """
    buf = mslice
    buf[1] = {3-2: 2+(2*4)-2}


def test_pyview_of_memview(int[:] ints):
    """
    >>> A = IntMockBuffer(None, [1, 2, 3])
    >>> len(test_pyview_of_memview(A))
    3
    """
    return ints


def test_generic_slicing(arg, indirect=False):
    """
    Test simple slicing
    >>> test_generic_slicing(IntMockBuffer("A", range(8 * 14 * 11), shape=(8, 14, 11)))
    acquired A
    (3, 9, 2)
    308 -11 1
    -1 -1 -1
    released A

    Test direct slicing, negative slice oob in dim 2
    >>> test_generic_slicing(IntMockBuffer("A", range(1 * 2 * 3), shape=(1, 2, 3)))
    acquired A
    (0, 0, 2)
    12 -3 1
    -1 -1 -1
    released A

    Test indirect slicing
    >>> test_generic_slicing(IntMockBuffer("A", shape_5_3_4_list, shape=(5, 3, 4)), indirect=True)
    acquired A
    (2, 0, 2)
    0 1 -1
    released A

    >>> stride1 = 21 * 14
    >>> stride2 = 21
    >>> test_generic_slicing(IntMockBuffer("A", shape_9_14_21_list, shape=(9, 14, 21)), indirect=True)
    acquired A
    (3, 9, 2)
    10 1 -1
    released A

    """
    cdef int[::view.generic, ::view.generic, :] _a = arg
    a = _a
    b = a[2:8:2, -4:1:-1, 1:3]

    print b.shape

    if indirect:
        print b.suboffsets[0] // sizeof(int *),
        print b.suboffsets[1] // sizeof(int),
        print b.suboffsets[2]
    else:
        print_int_offsets(b.strides[0], b.strides[1], b.strides[2])
        print_int_offsets(b.suboffsets[0], b.suboffsets[1], b.suboffsets[2])

    cdef int i, j, k
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                itemA = a[2 + 2 * i, -4 - j, 1 + k]
                itemB = b[i, j, k]
                assert itemA == itemB, (i, j, k, itemA, itemB)

def test_indirect_slicing(arg):
    """
    Test indirect slicing
    >>> test_indirect_slicing(IntMockBuffer("A", shape_5_3_4_list, shape=(5, 3, 4)))
    acquired A
    (5, 3, 2)
    0 0 -1
    58
    56
    58
    58
    58
    58
    released A

    >>> test_indirect_slicing(IntMockBuffer("A", shape_9_14_21_list, shape=(9, 14, 21)))
    acquired A
    (5, 14, 3)
    0 16 -1
    2412
    2410
    2412
    2412
    2412
    2412
    released A
    """
    cdef int[::view.indirect, ::view.indirect, :] _a = arg
    a = _a
    b = a[-5:, ..., -5:100:2]

    print b.shape
    print_int_offsets(*b.suboffsets)

    print b[4, 2, 1]
    print b[..., 0][4, 2]
    print b[..., 1][4, 2]
    print b[..., 1][4][2]
    print b[4][2][1]
    print b[4, 2][1]

def test_direct_slicing(arg):
    """
    Fused types would be convenient to test this stuff!

    Test simple slicing
    >>> test_direct_slicing(IntMockBuffer("A", range(8 * 14 * 11), shape=(8, 14, 11)))
    acquired A
    (3, 9, 2)
    308 -11 1
    -1 -1 -1
    released A

    Test direct slicing, negative slice oob in dim 2
    >>> test_direct_slicing(IntMockBuffer("A", range(1 * 2 * 3), shape=(1, 2, 3)))
    acquired A
    (0, 0, 2)
    12 -3 1
    -1 -1 -1
    released A
    """
    cdef int[:, :, :] _a = arg
    a = _a
    b = a[2:8:2, -4:1:-1, 1:3]

    print b.shape
    print_int_offsets(*b.strides)
    print_int_offsets(*b.suboffsets)

    cdef int i, j, k
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                itemA = a[2 + 2 * i, -4 - j, 1 + k]
                itemB = b[i, j, k]
                assert itemA == itemB, (i, j, k, itemA, itemB)


def test_slicing_and_indexing(arg):
    """
    >>> a = IntStridedMockBuffer("A", range(10 * 3 * 5), shape=(10, 3, 5))
    >>> test_slicing_and_indexing(a)
    acquired A
    (5, 2)
    15 2
    126 113
    [111]
    released A
    """
    cdef int[:, :, :] _a = arg
    a = _a
    b = a[-5:, 1, 1::2]
    c = b[4:1:-1, ::-1]
    d = c[2, 1:2]

    print b.shape
    print_int_offsets(*b.strides)

    cdef int i, j
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            itemA = a[-5 + i, 1, 1 + 2 * j]
            itemB = b[i, j]
            assert itemA == itemB, (i, j, itemA, itemB)

    print c[1, 1], c[2, 0]
    print [d[i] for i in range(d.shape[0])]

def test_oob():
    """
    >>> test_oob()
    Traceback (most recent call last):
       ...
    IndexError: Index out of bounds (axis 1)
    """
    cdef int[:, :] a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))
    print a[:, 20]

def test_acquire_memoryview():
    """
    Segfaulting in 3.2?
    >> test_acquire_memoryview()
    acquired A
    22
    <MemoryView of 'IntMockBuffer' object>
    22
    22
    released A
    """
    cdef int[:, :] a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))
    cdef object b = a

    print a[2, 4]

    # Make sure we don't have to keep this around
    del a

    print b
    cdef int[:, :] c = b
    print b[2, 4]
    print c[2, 4]

def test_acquire_memoryview_slice():
    """
    >>> test_acquire_memoryview_slice()
    acquired A
    31
    <MemoryView of 'IntMockBuffer' object>
    31
    31
    released A
    """
    cdef int[:, :] a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))
    a = a[1:, :6]

    cdef object b = a

    print a[2, 4]

    # Make sure we don't have to keep this around
    del a

    print b
    cdef int[:, :] c = b
    print b[2, 4]
    print c[2, 4]

class SingleObject(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == getattr(other, 'value', None) or self.value == other

def test_assign_scalar(int[:, :] m):
    """
    >>> A = IntMockBuffer("A", [0] * 100, shape=(10, 10))
    >>> test_assign_scalar(A)
    acquired A
    1 1 1 4 1 6 1 1 1 1
    2 2 2 4 2 6 2 2 2 2
    3 3 3 4 3 6 3 3 3 3
    1 1 1 4 1 6 1 1 1 1
    5 5 5 5 5 6 5 5 5 5
    1 1 1 4 1 6 1 1 1 1
    released A
    """
    m[:, :] = 1
    m[1, :] = 2
    m[2, :] = 3
    m[:, 3] = 4
    m[4, ...] = 5
    m[..., 5] = 6

    for i in range(6):
        print " ".join([str(m[i, j]) for j in range(m.shape[1])])


def test_contig_scalar_to_slice_assignment():
    """
    >>> test_contig_scalar_to_slice_assignment()
    14 14 14 14
    20 20 20 20
    """
    cdef int[5][10] a
    cdef int[:, ::1] _m = a
    m = _m

    m[...] = 14
    print m[0, 0], m[-1, -1], m[3, 2], m[4, 9]

    m[:, :] = 20
    print m[0, 0], m[-1, -1], m[3, 2], m[4, 9]

def test_dtype_object_scalar_assignment():
    """
    >>> test_dtype_object_scalar_assignment()
    """
    cdef object[:] m = array((10,), sizeof(PyObject *), 'O')
    m[:] = SingleObject(2)
    assert m[0] == m[4] == m[-1] == 2

    (<object> m)[:] = SingleObject(3)
    assert m[0] == m[4] == m[-1] == 3


def test_assignment_in_conditional_expression(bint left):
    """
    >>> test_assignment_in_conditional_expression(True)
    1.0
    2.0
    1.0
    2.0
    >>> test_assignment_in_conditional_expression(False)
    3.0
    4.0
    3.0
    4.0
    """
    cdef double a[2]
    cdef double b[2]
    a[:] = [1, 2]
    b[:] = [3, 4]

    cdef double[:] A = a
    cdef double[:] B = b
    cdef double[:] C, c

    # assign new memoryview references
    C = A if left else B

    for i in range(C.shape[0]):
        print C[i]

    # create new memoryviews
    c = a if left else b
    for i in range(c.shape[0]):
        print c[i]


def test_cpython_offbyone_issue_23349():
    """
    >>> print(test_cpython_offbyone_issue_23349())
    testing
    """
    cdef unsigned char[:] v = bytearray(b"testing")
    # the following returns 'estingt' without the workaround
    return bytearray(v).decode('ascii')


@cython.test_fail_if_path_exists('//SimpleCallNode')
@cython.test_assert_path_exists(
    '//ReturnStatNode//TupleNode',
    '//ReturnStatNode//TupleNode//CondExprNode',
)
def min_max_tree_restructuring():
    """
    >>> min_max_tree_restructuring()
    (1, 3)
    """
    cdef char a[5]
    a = [1, 2, 3, 4, 5]
    cdef char[:] aview = a

    return max(<char>1, aview[0]), min(<char>5, aview[2])


@cython.test_fail_if_path_exists(
    '//MemoryViewSliceNode',
)
@cython.test_assert_path_exists(
    '//MemoryViewIndexNode',
)
#@cython.boundscheck(False)  # reduce C code clutter
def optimised_index_of_slice(int[:,:,:] arr, int x, int y, int z):
    """
    >>> arr = IntMockBuffer("A", list(range(10*10*10)), shape=(10,10,10))
    >>> optimised_index_of_slice(arr, 2, 3, 4)
    acquired A
    (123, 123)
    (223, 223)
    (133, 133)
    (124, 124)
    (234, 234)
    (123, 123)
    (123, 123)
    (123, 123)
    (134, 134)
    (134, 134)
    (234, 234)
    (234, 234)
    (234, 234)
    released A
    """
    print(arr[1, 2, 3], arr[1][2][3])
    print(arr[x, 2, 3], arr[x][2][3])
    print(arr[1, y, 3], arr[1][y][3])
    print(arr[1, 2, z], arr[1][2][z])
    print(arr[x, y, z], arr[x][y][z])

    print(arr[1, 2, 3], arr[:, 2][1][3])
    print(arr[1, 2, 3], arr[:, 2, :][1, 3])
    print(arr[1, 2, 3], arr[:, 2, 3][1])
    print(arr[1, y, z], arr[1, :][y][z])
    print(arr[1, y, z], arr[1, :][y, z])

    print(arr[x, y, z], arr[x][:][:][y][:][:][z])
    print(arr[x, y, z], arr[:][x][:][y][:][:][z])
    print(arr[x, y, z], arr[:, :][x][:, :][y][:][z])


def test_assign_from_byteslike(byteslike):
    # Once http://python3statement.org is accepted, should be just
    # >>> test_assign_from_byteslike(bytes(b'hello'))
    # b'hello'
    # ...
    """
    >>> print(test_assign_from_byteslike(bytes(b'hello')).decode())
    hello
    >>> print(test_assign_from_byteslike(bytearray(b'howdy')).decode())
    howdy
    """
    # fails on Python 2.7- with
    #   TypeError: an integer is required
    # >>> print(test_assign_from_byteslike(pyarray.array('B', b'aloha')).decode())
    # aloha
    # fails on Python 2.6- with
    #   NameError: name 'memoryview' is not defined
    # >>> print(test_assign_from_byteslike(memoryview(b'bye!!')).decode())
    # bye!!

    def assign(m):
        m[:] = byteslike

    cdef void *buf
    cdef unsigned char[:] mview
    buf = malloc(5)
    try:
        mview = <unsigned char[:5]>(buf)
        assign(mview)
        return (<unsigned char*>buf)[:5]
    finally:
        free(buf)
