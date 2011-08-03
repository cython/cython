# mode: run

u'''
>>> f()
>>> g()
>>> call()
>>> assignmvs()
'''

from cython.view cimport memoryview
from cython cimport array, PyBUF_C_CONTIGUOUS
from cython cimport view

include "mockbuffers.pxi"

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

cdef int[:] func():
    pass

cdef ExtClass get_ext_obj():
    print 'get_ext_obj called'
    return ExtClass.__new__(ExtClass)

def test_cdef_attribute():
    """
    >>> test_cdef_attribute()
    Memoryview is not initialized
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

    # uninitialized assignment is valid
    cdef int[:] otherview = myview

    try:
        print get_ext_obj().mview
    except AttributeError, e:
        print e.args[0]
    else:
        print "No AttributeError was raised"

    print ExtClass().mview

'''
def basic_struct(MyStruct[:] mslice):
    """
    See also buffmt.pyx

    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="bbqii"))
    1 2 3 4 5
    """
    buf = mslice
    print buf[0].a, buf[0].b, buf[0].c, buf[0].d, buf[0].e

def nested_struct(NestedStruct[:] mslice):
    """
    See also buffmt.pyx

    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="T{ii}T{2i}i"))
    1 2 3 4 5
    """
    buf = mslice
    print buf[0].x.a, buf[0].x.b, buf[0].y.a, buf[0].y.b, buf[0].z

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
    print buf[0].a, buf[0].b

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
    print buf[0].a, buf[0].b, buf[0].sub.a, buf[0].sub.b, buf[0].c


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
    print buf[0].real, buf[0].imag

def complex_struct_inplace(LongComplex[:] mslice):
    """
    >>> complex_struct_inplace(LongComplexMockBuffer(None, [(0, -1)]))
    1.0 1.0
    """
    buf = mslice
    buf[0].real += 1
    buf[0].imag += 2
    print buf[0].real, buf[0].imag
'''
#
# Getting items and index bounds checking
#
def get_int_2d(int[:, :] mslice, int i, int j):
    """
    >>> C = IntMockBuffer("C", range(6), (2,3))
    >>> get_int_2d(C, 1, 1)
    acquired C
    acquired C
    released C
    released C
    4

    Check negative indexing:
    >>> get_int_2d(C, -1, 0)
    acquired C
    acquired C
    released C
    released C
    3
    >>> get_int_2d(C, -1, -2)
    acquired C
    acquired C
    released C
    released C
    4
    >>> get_int_2d(C, -2, -3)
    acquired C
    acquired C
    released C
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
    acquired C
    released C
    released C
    >>> get_int_2d(C, 1, 1)
    acquired C
    acquired C
    released C
    released C
    10

    Check negative indexing:
    >>> set_int_2d(C, -1, 0, 3)
    acquired C
    acquired C
    released C
    released C
    >>> get_int_2d(C, -1, 0)
    acquired C
    acquired C
    released C
    released C
    3

    >>> set_int_2d(C, -1, -2, 8)
    acquired C
    acquired C
    released C
    released C
    >>> get_int_2d(C, -1, -2)
    acquired C
    acquired C
    released C
    released C
    8

    >>> set_int_2d(C, -2, -3, 9)
    acquired C
    acquired C
    released C
    released C
    >>> get_int_2d(C, -2, -3)
    acquired C
    acquired C
    released C
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
    acquired R
    released R
    released R
    >>> [str(x) for x in R.recieved_flags] # Py2/3
    ['FORMAT', 'ND', 'STRIDES', 'WRITABLE']
    """
    buf = mslice
    buf[2, 2, 1] = 23

def strided(int[:] mslice):
    """
    >>> A = IntMockBuffer("A", range(4))
    >>> strided(A)
    acquired A
    acquired A
    released A
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
    Multi-dim has seperate implementation

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
    acquired A
    acquired B
    4
    4
    10
    11
    released A
    released B
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

def generic_contig(int[::view.generic_contiguous, :] mslice1,
                   int[::view.generic_contiguous, :] mslice2):
    """
    >>> A = IntMockBuffer("A", [[0,1,2], [3,4,5], [6,7,8]])
    >>> B = IntMockBuffer("B", [[0,1,2], [3,4,5], [6,7,8]], shape=(3, 3), strides=(1, 3))
    >>> generic_contig(A, B)
    acquired A
    acquired B
    acquired A
    acquired B
    4
    4
    10
    11
    released A
    released B
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
