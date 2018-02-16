# Tests the buffer access syntax functionality by constructing
# mock buffer objects.
#
# Note that the buffers are mock objects created for testing
# the buffer access behaviour -- for instance there is no flag
# checking in the buffer objects (why test our test case?), rather
# what we want to test is what is passed into the flags argument.
#

from __future__ import unicode_literals

from cpython.object cimport PyObject
from cpython.ref cimport Py_INCREF, Py_DECREF
cimport cython

__test__ = {}

import sys
#import re
exclude = []#re.compile('object').search]

if getattr(sys, 'pypy_version_info', None) is not None:
    # disable object-in-buffer tests in PyPy
    import re
    exclude.append(re.compile('object').search)

def testcase(func):
    for e in exclude:
        if e(func.__name__):
            return func
    __test__[func.__name__] = func.__doc__
    return func


include "mockbuffers.pxi"

#
# Buffer acquire and release tests
#

def nousage():
    """
    The challenge here is just compilation.
    """
    cdef object[int, ndim=2] buf


@testcase
def disabled_usage(obj):
    """
    The challenge here is just compilation.

    >>> disabled_usage(None)
    """
    cdef object[int, ndim=2] buf
    if False:
        buf = obj
    return obj


@testcase
def nousage_cleanup(x):
    """
    >>> nousage_cleanup(False)
    >>> nousage_cleanup(True)
    Traceback (most recent call last):
    RuntimeError
    """
    cdef object[int, ndim=2] buf
    if x:
        raise RuntimeError()


@testcase
def acquire_release(o1, o2):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> B = IntMockBuffer("B", range(6))
    >>> acquire_release(A, B)
    acquired A
    released A
    acquired B
    released B
    >>> acquire_release(None, None)
    >>> acquire_release(None, B)
    acquired B
    released B
    """
    cdef object[int] buf
    buf = o1
    buf = o2

@testcase
def acquire_raise(o):
    """
    Apparently, doctest won't handle mixed exceptions and print
    stats, so need to circumvent this.

    >>> A = IntMockBuffer("A", range(6))
    >>> A.resetlog()
    >>> acquire_raise(A)
    Traceback (most recent call last):
        ...
    Exception: on purpose
    >>> A.printlog()
    acquired A
    released A

    """
    cdef object[int] buf
    buf = o
    raise Exception("on purpose")

@testcase
def acquire_failure1():
    """
    >>> acquire_failure1()
    acquired working
    0 3
    0 3
    released working
    """
    cdef object[int] buf
    buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = ErrorBuffer()
        assert False
    except Exception:
        print buf[0], buf[3]

@testcase
def acquire_failure2():
    """
    >>> acquire_failure2()
    acquired working
    0 3
    0 3
    released working
    """
    cdef object[int] buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = ErrorBuffer()
        assert False
    except Exception:
        print buf[0], buf[3]

@testcase
def acquire_failure3():
    """
    >>> acquire_failure3()
    acquired working
    0 3
    released working
    acquired working
    0 3
    released working
    """
    cdef object[int] buf
    buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = 3
        assert False
    except Exception:
        print buf[0], buf[3]

@testcase
def acquire_failure4():
    """
    >>> acquire_failure4()
    acquired working
    0 3
    released working
    acquired working
    0 3
    released working
    """
    cdef object[int] buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = 2
        assert False
    except Exception:
        print buf[0], buf[3]

@testcase
def acquire_failure5():
    """
    >>> acquire_failure5()
    Traceback (most recent call last):
       ...
    ValueError: Buffer acquisition failed on assignment; and then reacquiring the old buffer failed too!
    """
    cdef object[int] buf
    buf = IntMockBuffer("working", range(4))
    buf.fail = True
    buf = 3


@testcase
def acquire_nonbuffer1(first, second=None):
    """
    >>> acquire_nonbuffer1(3)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:... 'int'...
    >>> acquire_nonbuffer1(type)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:... 'type'...
    >>> acquire_nonbuffer1(None, 2)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError:... 'int'...
    """
    cdef object[int] buf
    buf = first
    buf = second

@testcase
def acquire_nonbuffer2():
    """
    >>> acquire_nonbuffer2()
    acquired working
    0 3
    released working
    acquired working
    0 3
    released working
    """
    cdef object[int] buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = ErrorBuffer
        assert False
    except Exception:
        print buf[0], buf[3]


@testcase
def as_argument(object[int] bufarg, int n):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> as_argument(A, 6)
    acquired A
    0 1 2 3 4 5 END
    released A
    """
    cdef int i
    for i in range(n):
        print bufarg[i],
    print 'END'

@testcase
def as_argument_not_none(object[int] bufarg not None):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> as_argument_not_none(A)
    acquired A
    ACCEPTED
    released A
    >>> as_argument_not_none(None)
    Traceback (most recent call last):
    TypeError: Argument 'bufarg' must not be None
    """
    print 'ACCEPTED'

@testcase
def as_argument_defval(object[int] bufarg=IntMockBuffer('default', range(6)), int n=6):
    """
    >>> as_argument_defval()
    acquired default
    0 1 2 3 4 5 END
    released default
    >>> A = IntMockBuffer("A", range(6))
    >>> as_argument_defval(A, 6)
    acquired A
    0 1 2 3 4 5 END
    released A
    """
    cdef int i
    for i in range(n):
        print bufarg[i],
    print 'END'

@testcase
def cdef_assignment(obj, n):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> cdef_assignment(A, 6)
    acquired A
    0 1 2 3 4 5 END
    released A

    """
    cdef object[int] buf = obj
    cdef int i
    for i in range(n):
        print buf[i],
    print 'END'

@testcase
def forin_assignment(objs, int pick):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> B = IntMockBuffer("B", range(6))
    >>> forin_assignment([A, B, A, A], 2)
    acquired A
    2
    released A
    acquired B
    2
    released B
    acquired A
    2
    released A
    acquired A
    2
    released A
    """
    cdef object[int] buf
    for buf in objs:
        print buf[pick]

@testcase
def cascaded_buffer_assignment(obj):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> cascaded_buffer_assignment(A)
    acquired A
    acquired A
    released A
    released A
    """
    cdef object[int] a, b
    a = b = obj

@testcase
def tuple_buffer_assignment1(a, b):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> B = IntMockBuffer("B", range(6))
    >>> tuple_buffer_assignment1(A, B)
    acquired A
    acquired B
    released A
    released B
    """
    cdef object[int] x, y
    x, y = a, b

@testcase
def tuple_buffer_assignment2(tup):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> B = IntMockBuffer("B", range(6))
    >>> tuple_buffer_assignment2((A, B))
    acquired A
    acquired B
    released A
    released B
    """
    cdef object[int] x, y
    x, y = tup

@testcase
def explicitly_release_buffer():
    """
    >>> explicitly_release_buffer()
    acquired A
    released A
    After release
    """
    cdef object[int] x = IntMockBuffer("A", range(10))
    x = None
    print "After release"

#
# Getting items and index bounds checking
#
@testcase
def get_int_2d(object[int, ndim=2] buf, int i, int j):
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
    return buf[i, j]

@testcase
def get_int_2d_uintindex(object[int, ndim=2] buf, unsigned int i, unsigned int j):
    """
    Unsigned indexing:
    >>> C = IntMockBuffer("C", range(6), (2,3))
    >>> get_int_2d_uintindex(C, 0, 0)
    acquired C
    released C
    0
    >>> get_int_2d_uintindex(C, 1, 2)
    acquired C
    released C
    5
    """
    # This is most interesting with regards to the C code
    # generated.
    return buf[i, j]

@testcase
def set_int_2d(object[int, ndim=2] buf, int i, int j, int value):
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
    buf[i, j] = value

@testcase
def set_int_2d_cascaded(object[int, ndim=2] buf, int i, int j, int value):
    """
    Uses get_int_2d to read back the value afterwards. For pure
    unit test, one should support reading in MockBuffer instead.

    >>> C = IntMockBuffer("C", range(6), (2,3))
    >>> set_int_2d_cascaded(C, 1, 1, 10)
    acquired C
    released C
    10
    >>> get_int_2d(C, 1, 1)
    acquired C
    released C
    10

    Check negative indexing:
    >>> set_int_2d_cascaded(C, -1, 0, 3)
    acquired C
    released C
    3
    >>> get_int_2d(C, -1, 0)
    acquired C
    released C
    3

    >>> set_int_2d_cascaded(C, -1, -2, 8)
    acquired C
    released C
    8
    >>> get_int_2d(C, -1, -2)
    acquired C
    released C
    8

    >>> set_int_2d_cascaded(C, -2, -3, 9)
    acquired C
    released C
    9
    >>> get_int_2d(C, -2, -3)
    acquired C
    released C
    9

    Out-of-bounds errors:
    >>> set_int_2d_cascaded(C, 2, 0, 19)
    Traceback (most recent call last):
    IndexError: Out of bounds on buffer access (axis 0)
    >>> set_int_2d_cascaded(C, 0, -4, 19)
    Traceback (most recent call last):
    IndexError: Out of bounds on buffer access (axis 1)

    """
    cdef int casc_value
    buf[i, j] = casc_value = value
    return casc_value

@testcase
def list_comprehension(object[int] buf, len):
    """
    >>> list_comprehension(IntMockBuffer(None, [1,2,3]), 3)
    1|2|3
    """
    cdef int i
    print u"|".join([unicode(buf[i]) for i in range(len)])

#
# The negative_indices buffer option
#
@testcase
def no_negative_indices(object[int, negative_indices=False] buf, int idx):
    """
    The most interesting thing here is to inspect the C source and
    make sure optimal code is produced.

    >>> A = IntMockBuffer(None, range(6))
    >>> no_negative_indices(A, 3)
    3
    >>> no_negative_indices(A, -1)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    """
    return buf[idx]

@testcase
@cython.wraparound(False)
def wraparound_directive(object[int] buf, int pos_idx, int neg_idx):
    """
    Again, the most interesting thing here is to inspect the C source.

    >>> A = IntMockBuffer(None, range(4))
    >>> wraparound_directive(A, 2, -1)
    5
    >>> wraparound_directive(A, -1, 2)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    """
    cdef int byneg
    with cython.wraparound(True):
        byneg = buf[neg_idx]
    return buf[pos_idx] + byneg


#
# Test which flags are passed.
#
@testcase
def readonly(obj):
    """
    >>> R = UnsignedShortMockBuffer("R", range(27), shape=(3, 3, 3))
    >>> readonly(R)
    acquired R
    25
    released R
    >>> [str(x) for x in R.received_flags]  # Works in both py2 and py3
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES']
    """
    cdef object[unsigned short int, ndim=3] buf = obj
    print buf[2, 2, 1]

@testcase
def writable(obj):
    """
    >>> R = UnsignedShortMockBuffer("R", range(27), shape=(3, 3, 3))
    >>> writable(R)
    acquired R
    released R
    >>> [str(x) for x in R.received_flags] # Py2/3
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    """
    cdef object[unsigned short int, ndim=3] buf = obj
    buf[2, 2, 1] = 23

@testcase
def strided(object[int, ndim=1, mode='strided'] buf):
    """
    >>> A = IntMockBuffer("A", range(4))
    >>> strided(A)
    acquired A
    released A
    2
    >>> [str(x) for x in A.received_flags] # Py2/3
    ['FORMAT', 'ND', 'STRIDES']

    Check that the suboffsets were patched back prior to release.
    >>> A.release_ok
    True
    """
    return buf[2]

@testcase
def c_contig(object[int, ndim=1, mode='c'] buf):
    """
    >>> A = IntMockBuffer(None, range(4))
    >>> c_contig(A)
    2
    >>> [str(x) for x in A.received_flags]
    ['FORMAT', 'ND', 'STRIDES', 'C_CONTIGUOUS']
    """
    return buf[2]

@testcase
def c_contig_2d(object[int, ndim=2, mode='c'] buf):
    """
    Multi-dim has separate implementation

    >>> A = IntMockBuffer(None, range(12), shape=(3,4))
    >>> c_contig_2d(A)
    7
    >>> [str(x) for x in A.received_flags]
    ['FORMAT', 'ND', 'STRIDES', 'C_CONTIGUOUS']
    """
    return buf[1, 3]

@testcase
def f_contig(object[int, ndim=1, mode='fortran'] buf):
    """
    >>> A = IntMockBuffer(None, range(4))
    >>> f_contig(A)
    2
    >>> [str(x) for x in A.received_flags]
    ['FORMAT', 'ND', 'STRIDES', 'F_CONTIGUOUS']
    """
    return buf[2]

@testcase
def f_contig_2d(object[int, ndim=2, mode='fortran'] buf):
    """
    Must set up strides manually to ensure Fortran ordering.

    >>> A = IntMockBuffer(None, range(12), shape=(4,3), strides=(1, 4))
    >>> f_contig_2d(A)
    7
    >>> [str(x) for x in A.received_flags]
    ['FORMAT', 'ND', 'STRIDES', 'F_CONTIGUOUS']
    """
    return buf[3, 1]

#
# Test compiler options for bounds checking. We create an array with a
# safe "boundary" (memory
# allocated outside of what it published) and then check whether we get back
# what we stored in the memory or an error.

@testcase
def safe_get(object[int] buf, int idx):
    """
    >>> A = IntMockBuffer(None, range(10), shape=(3,), offset=5)

    Validate our testing buffer...
    >>> safe_get(A, 0)
    5
    >>> safe_get(A, 2)
    7
    >>> safe_get(A, -3)
    5

    Access outside it. This is already done above for bounds check
    testing but we include it to tell the story right.

    >>> safe_get(A, -4)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    >>> safe_get(A, 3)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    """
    return buf[idx]

@testcase
@cython.boundscheck(False) # outer decorators should take precedence
@cython.boundscheck(True)
def unsafe_get(object[int] buf, int idx):
    """
    Access outside of the area the buffer publishes.
    >>> A = IntMockBuffer(None, range(10), shape=(3,), offset=5)
    >>> unsafe_get(A, -4)
    4
    >>> unsafe_get(A, -5)
    3
    >>> unsafe_get(A, 3)
    8
    """
    return buf[idx]

@testcase
@cython.boundscheck(False)
def unsafe_get_nonegative(object[int, negative_indices=False] buf, int idx):
    """
    Also inspect the C source to see that it is optimal...

    >>> A = IntMockBuffer(None, range(10), shape=(3,), offset=5)
    >>> unsafe_get_nonegative(A, -2)
    3
    """
    return buf[idx]

@testcase
def mixed_get(object[int] buf, int unsafe_idx, int safe_idx):
    """
    >>> A = IntMockBuffer(None, range(10), shape=(3,), offset=5)
    >>> mixed_get(A, -4, 0)
    (4, 5)
    >>> mixed_get(A, 0, -4)
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    """
    with cython.boundscheck(False):
        one = buf[unsafe_idx]
    with cython.boundscheck(True):
        two = buf[safe_idx]
    return (one, two)

#
# Coercions
#
## @testcase
## def coercions(object[unsigned char] uc):
##     """
## TODO
##     """
##     print type(uc[0])
##     uc[0] = -1
##     print uc[0]
##     uc[0] = <int>3.14
##     print uc[0]

##     cdef char* ch = b"asfd"
##     cdef object[object] objbuf
##     objbuf[3] = ch


#
# Testing that accessing data using various types of buffer access
# all works.
#

def printbuf_int(object[int] buf, shape):
    # Utility func
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'


@testcase
def printbuf_int_2d(o, shape):
    """
    Strided:

    >>> printbuf_int_2d(IntMockBuffer("A", range(6), (2,3)), (2,3))
    acquired A
    0 1 2 END
    3 4 5 END
    released A
    >>> printbuf_int_2d(IntMockBuffer("A", range(100), (3,3), strides=(20,5)), (3,3))
    acquired A
    0 5 10 END
    20 25 30 END
    40 45 50 END
    released A

    Indirect:
    >>> printbuf_int_2d(IntMockBuffer("A", [[1,2],[3,4]]), (2,2))
    acquired A
    1 2 END
    3 4 END
    released A
    """
    # should make shape builtin
    cdef object[int, ndim=2] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        for j in range(shape[1]):
            print buf[i, j],
        print 'END'

@testcase
def printbuf_float(o, shape):
    """
    >>> printbuf_float(FloatMockBuffer("F", [1.0, 1.25, 0.75, 1.0]), (4,))
    acquired F
    1.0 1.25 0.75 1.0 END
    released F
    """

    # should make shape builtin
    cdef object[float] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        print buf[i],
    print "END"


#
# Test assignments
#
@testcase
def inplace_operators(object[int] buf):
    """
    >>> buf = IntMockBuffer(None, [2, 2])
    >>> inplace_operators(buf)
    >>> printbuf_int(buf, (2,))
    0 3 END
    """
    cdef int j = 0
    buf[1] += 1
    buf[j] *= 2
    buf[0] -= 4



#
# Typedefs
#
# Test three layers of typedefs going through a h file for plain int, and
# simply a header file typedef for floats and unsigned.

ctypedef int td_cy_int
cdef extern from "bufaccess.h":
    ctypedef td_cy_int td_h_short # Defined as short, but Cython doesn't know this!
    ctypedef float td_h_double # Defined as double
    ctypedef unsigned int td_h_ushort # Defined as unsigned short
ctypedef td_h_short td_h_cy_short

@testcase
def printbuf_td_cy_int(object[td_cy_int] buf, shape):
    """
    >>> printbuf_td_cy_int(IntMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_cy_int(ShortMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_cy_int' but got 'short'
    """
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

@testcase
def printbuf_td_h_short(object[td_h_short] buf, shape):
    """
    >>> printbuf_td_h_short(ShortMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_h_short(IntMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_short' but got 'int'
    """
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

@testcase
def printbuf_td_h_cy_short(object[td_h_cy_short] buf, shape):
    """
    >>> printbuf_td_h_cy_short(ShortMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_h_cy_short(IntMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_cy_short' but got 'int'
    """
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

@testcase
def printbuf_td_h_ushort(object[td_h_ushort] buf, shape):
    """
    >>> printbuf_td_h_ushort(UnsignedShortMockBuffer(None, range(3)), (3,))
    0 1 2 END
    >>> printbuf_td_h_ushort(ShortMockBuffer(None, range(3)), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_ushort' but got 'short'
    """
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'

@testcase
def printbuf_td_h_double(object[td_h_double] buf, shape):
    """
    >>> printbuf_td_h_double(DoubleMockBuffer(None, [0.25, 1, 3.125]), (3,))
    0.25 1.0 3.125 END
    >>> printbuf_td_h_double(FloatMockBuffer(None, [0.25, 1, 3.125]), (3,))
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'td_h_double' but got 'float'
    """
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

@testcase
def printbuf_object(object[object] buf, shape):
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
    cdef int i
    for i in range(shape[0]):
        print repr(buf[i]), (<PyObject*>buf[i]).ob_refcnt

@testcase
def assign_to_object(object[object] buf, int idx, obj):
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
    buf[idx] = obj

@testcase
def assign_temporary_to_object(object[object] buf):
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
    buf[1] = {3-2: 2+(2*4)-2}

#
# cast option
#
@testcase
def buffer_cast(object[unsigned int, cast=True] buf, int idx):
    """
    Round-trip a signed int through unsigned int buffer access.

    >>> A = IntMockBuffer(None, [-100])
    >>> buffer_cast(A, 0)
    -100
    """
    cdef unsigned int data = buf[idx]
    return <int>data

@testcase
def buffer_cast_fails(object[char, cast=True] buf):
    """
    Cannot cast between datatype of different sizes.

    >>> buffer_cast_fails(IntMockBuffer(None, [0]))
    Traceback (most recent call last):
        ...
    ValueError: Item size of buffer (4 bytes) does not match size of 'char' (1 byte)
    """
    return buf[0]

#
# Typed buffers
#
@testcase
def typedbuffer1(obj):
    """
    >>> typedbuffer1(IntMockBuffer("A", range(10)))
    acquired A
    released A
    >>> typedbuffer1(None)
    >>> typedbuffer1(4)
    Traceback (most recent call last):
       ...
    TypeError: Cannot convert int to bufaccess.IntMockBuffer
    """
    cdef IntMockBuffer[int, ndim=1] buf = obj

@testcase
def typedbuffer2(IntMockBuffer[int, ndim=1] obj):
    """
    >>> typedbuffer2(IntMockBuffer("A", range(10)))
    acquired A
    released A
    >>> typedbuffer2(None)
    >>> typedbuffer2(4)
    Traceback (most recent call last):
       ...
    TypeError: Argument 'obj' has incorrect type (expected bufaccess.IntMockBuffer, got int)
    """
    pass

#
# Test __cythonbufferdefaults__
#
@testcase
def bufdefaults1(IntStridedMockBuffer[int, ndim=1] buf):
    """
    For IntStridedMockBuffer, mode should be
    "strided" by defaults which should show
    up in the flags.

    >>> A = IntStridedMockBuffer("A", range(10))
    >>> bufdefaults1(A)
    acquired A
    released A
    >>> [str(x) for x in A.received_flags]
    ['FORMAT', 'ND', 'STRIDES']
    """
    pass


@testcase
def basic_struct(object[MyStruct] buf):
    """
    See also buffmt.pyx

    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="ccqii"))
    1 2 3 4 5
    """
    print buf[0].a, buf[0].b, buf[0].c, buf[0].d, buf[0].e

@testcase
def nested_struct(object[NestedStruct] buf):
    """
    See also buffmt.pyx

    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="T{ii}T{2i}i"))
    1 2 3 4 5
    """
    print buf[0].x.a, buf[0].x.b, buf[0].y.a, buf[0].y.b, buf[0].z

@testcase
def packed_struct(object[PackedStruct] buf):
    """
    See also buffmt.pyx

    >>> packed_struct(PackedStructMockBuffer(None, [(1, 2)]))
    1 2
    >>> packed_struct(PackedStructMockBuffer(None, [(1, 2)], format="T{c^i}"))
    1 2
    >>> packed_struct(PackedStructMockBuffer(None, [(1, 2)], format="T{c=i}"))
    1 2

    """
    print buf[0].a, buf[0].b

@testcase
def nested_packed_struct(object[NestedPackedStruct] buf):
    """
    See also buffmt.pyx

    >>> nested_packed_struct(NestedPackedStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> nested_packed_struct(NestedPackedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="ci^ci@i"))
    1 2 3 4 5
    >>> nested_packed_struct(NestedPackedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="^c@i^ci@i"))
    1 2 3 4 5
    """
    print buf[0].a, buf[0].b, buf[0].sub.a, buf[0].sub.b, buf[0].c


@testcase
def complex_dtype(object[long double complex] buf):
    """
    >>> complex_dtype(LongComplexMockBuffer(None, [(0, -1)]))
    -1j
    """
    print buf[0]

@testcase
def complex_inplace(object[long double complex] buf):
    """
    >>> complex_inplace(LongComplexMockBuffer(None, [(0, -1)]))
    (1+1j)
    """
    buf[0] = buf[0] + 1 + 2j
    print buf[0]

@testcase
def complex_struct_dtype(object[LongComplex] buf):
    """
    Note that the format string is "Zg" rather than "2g", yet a struct
    is accessed.
    >>> complex_struct_dtype(LongComplexMockBuffer(None, [(0, -1)]))
    0.0 -1.0
    """
    print buf[0].real, buf[0].imag

@testcase
def complex_struct_inplace(object[LongComplex] buf):
    """
    >>> complex_struct_inplace(LongComplexMockBuffer(None, [(0, -1)]))
    1.0 1.0
    """
    buf[0].real += 1
    buf[0].imag += 2
    print buf[0].real, buf[0].imag

#
# Nogil
#
@testcase
@cython.boundscheck(False)
def buffer_nogil():
    """
    >>> buffer_nogil()
    10
    """
    cdef object[int] buf = IntMockBuffer(None, [1,2,3])
    with nogil:
        buf[1] = 10
    return buf[1]

@testcase
def buffer_nogil_oob():
    """
    >>> buffer_nogil_oob()
    Traceback (most recent call last):
        ...
    IndexError: Out of bounds on buffer access (axis 0)
    """
    cdef object[int] buf = IntMockBuffer(None, [1,2,3])
    with nogil:
        buf[5] = 10
    return buf[1]

def get_int():
    return 10

@testcase
def test_inplace_assignment():
    """
    >>> test_inplace_assignment()
    10
    """
    cdef object[int, ndim=1] buf = IntMockBuffer(None, [1, 2, 3])

    buf[0] = get_int()
    print buf[0]

@testcase
def test_nested_assignment():
    """
    >>> test_nested_assignment()
    100
    """
    cdef object[int] inner = IntMockBuffer(None, [1, 2, 3])
    cdef object[int] outer = IntMockBuffer(None, [1, 2, 3])
    outer[inner[0]] = 100
    return outer[inner[0]]
