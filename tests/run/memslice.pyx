# mode: run

# Note: see also bufaccess.pyx

from __future__ import unicode_literals

cimport cython
from cython cimport view
from cython.parallel cimport prange

print cython.array

import sys
import re

__test__ = {}

def testcase(func):
    doctest = func.__doc__
    if sys.version_info >= (3,1,1):
        doctest = doctest.replace('does not have the buffer interface',
                                  'does not support the buffer interface')
    if sys.version_info >= (3, 0):
        _u = str
    else:
        _u = unicode
    if not isinstance(doctest, _u):
        doctest = doctest.decode('UTF-8')
    __test__[func.__name__] = doctest
    return func


include "mockbuffers.pxi"
include "cythonarrayutil.pxi"

#
# Buffer acquire and release tests
#

def nousage():
    """
    The challenge here is just compilation.
    """
    cdef int[:, :] buf

@testcase
def acquire_release(o1, o2):
    """
    >>> A = IntMockBuffer("A", range(6))
    >>> B = IntMockBuffer("B", range(6))
    >>> acquire_release(A, B)
    acquired A
    acquired B
    released A
    released B
    >>> acquire_release(None, B)
    Traceback (most recent call last):
       ...
    TypeError: 'NoneType' does not have the buffer interface
    """
    cdef int[:] buf
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
    cdef int[:] buf
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
    cdef int[:] buf
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
    cdef int[:] buf = IntMockBuffer("working", range(4))
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
    0 3
    released working
    """
    cdef int[:] buf
    buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = object()
        assert False
    except Exception:
        print buf[0], buf[3]

@testcase
def acquire_nonbuffer1(first, second=None):
    """
    >>> acquire_nonbuffer1(3)
    Traceback (most recent call last):
      ...
    TypeError: 'int' does not have the buffer interface
    >>> acquire_nonbuffer1(type)
    Traceback (most recent call last):
      ...
    TypeError: 'type' does not have the buffer interface
    >>> acquire_nonbuffer1(None, 2)
    Traceback (most recent call last):
      ...
    TypeError: 'NoneType' does not have the buffer interface
    >>> acquire_nonbuffer1(4, object())
    Traceback (most recent call last):
      ...
    TypeError: 'int' does not have the buffer interface
    """
    cdef int[:] buf
    buf = first
    buf = second

@testcase
def acquire_nonbuffer2():
    """
    >>> acquire_nonbuffer2()
    acquired working
    0 3
    0 3
    released working
    """
    cdef int[:] buf = IntMockBuffer("working", range(4))
    print buf[0], buf[3]
    try:
        buf = ErrorBuffer
        assert False
    except Exception:
        print buf[0], buf[3]

@testcase
def as_argument(int[:] bufarg, int n):
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
def as_argument_defval(int[:] bufarg=IntMockBuffer('default', range(6)), int n=6):
    """
    >>> as_argument_defval()
    0 1 2 3 4 5 END
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
    cdef int[:] buf = obj
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
    acquired B
    released A
    2
    acquired A
    released B
    2
    acquired A
    released A
    2
    released A
    """
    cdef int[:] buf
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
    cdef int[:] a, b
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
    cdef int[:] x, y
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
    cdef int[:] x, y
    x, y = tup

@testcase
def explicitly_release_buffer():
    """
    >>> explicitly_release_buffer()
    acquired A
    released A
    After release
    """
    cdef int[:] x = IntMockBuffer("A", range(10))
    del x
    print "After release"

#
# Getting items and index bounds checking
#
@testcase
def get_int_2d(int[:, :] buf, int i, int j):
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
def get_int_2d_uintindex(int[:, :] buf, unsigned int i, unsigned int j):
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
def set_int_2d(int[:, :] buf, int i, int j, int value):
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
def list_comprehension(int[:] buf, len):
    """
    >>> list_comprehension(IntMockBuffer(None, [1,2,3]), 3)
    1|2|3
    """
    cdef int i
    print u"|".join([unicode(buf[i]) for i in range(len)])

@testcase
@cython.wraparound(False)
def wraparound_directive(int[:] buf, int pos_idx, int neg_idx):
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
# Test all kinds of indexing and flags
#

@testcase
def writable(obj):
    """
    >>> R = UnsignedShortMockBuffer("R", range(27), shape=(3, 3, 3))
    >>> writable(R)
    acquired R
    released R
    >>> [str(x) for x in R.recieved_flags] # Py2/3
    ['FORMAT', 'ND', 'STRIDES', 'WRITABLE']
    """
    cdef unsigned short int[:, :, :] buf = obj
    buf[2, 2, 1] = 23

@testcase
def strided(int[:] buf):
    """
    >>> A = IntMockBuffer("A", range(4))
    >>> strided(A)
    acquired A
    released A
    2
    >>> [str(x) for x in A.recieved_flags] # Py2/3
    ['FORMAT', 'ND', 'STRIDES', 'WRITABLE']

    Check that the suboffsets were patched back prior to release.
    >>> A.release_ok
    True
    """
    return buf[2]

@testcase
def c_contig(int[::1] buf):
    """
    >>> A = IntMockBuffer(None, range(4))
    >>> c_contig(A)
    2
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'C_CONTIGUOUS', 'WRITABLE']
    """
    return buf[2]

@testcase
def c_contig_2d(int[:, ::1] buf):
    """
    Multi-dim has seperate implementation

    >>> A = IntMockBuffer(None, range(12), shape=(3,4))
    >>> c_contig_2d(A)
    7
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'C_CONTIGUOUS', 'WRITABLE']
    """
    return buf[1, 3]

@testcase
def f_contig(int[::1, :] buf):
    """
    >>> A = IntMockBuffer(None, range(4), shape=(2, 2), strides=(1, 2))
    >>> f_contig(A)
    2
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'F_CONTIGUOUS', 'WRITABLE']
    """
    return buf[0, 1]

@testcase
def f_contig_2d(int[::1, :] buf):
    """
    Must set up strides manually to ensure Fortran ordering.

    >>> A = IntMockBuffer(None, range(12), shape=(4,3), strides=(1, 4))
    >>> f_contig_2d(A)
    7
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'F_CONTIGUOUS', 'WRITABLE']
    """
    return buf[3, 1]

@testcase
def generic(int[::view.generic, ::view.generic] buf1,
            int[::view.generic, ::view.generic] buf2):
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
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    >>> [str(x) for x in B.recieved_flags]
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    """
    print buf1[1, 1]
    print buf2[1, 1]

    buf1[2, -1] = 10
    buf2[2, -1] = 11

    print buf1[2, 2]
    print buf2[2, 2]

# Note: disabled. generic_contiguous isn't very useful (you have to check suboffsets,
#                                                       might as well multiply with strides)
# def generic_contig(int[::view.generic_contiguous, :] buf1,
#                    int[::view.generic_contiguous, :] buf2):
#     """
#     >>> A = IntMockBuffer("A", [[0,1,2], [3,4,5], [6,7,8]])
#     >>> B = IntMockBuffer("B", [[0,1,2], [3,4,5], [6,7,8]], shape=(3, 3), strides=(1, 3))
#     >>> generic_contig(A, B)
#     acquired A
#     acquired B
#     4
#     4
#     10
#     11
#     released A
#     released B
#     >>> [str(x) for x in A.recieved_flags]
#     ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
#     >>> [str(x) for x in B.recieved_flags]
#     ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
#     """
#     print buf1[1, 1]
#     print buf2[1, 1]
#
#     buf1[2, -1] = 10
#     buf2[2, -1] = 11
#
#     print buf1[2, 2]
#     print buf2[2, 2]

@testcase
def indirect_strided_and_contig(
             int[::view.indirect, ::view.strided] buf1,
             int[::view.indirect, ::view.contiguous] buf2):
    """
    >>> A = IntMockBuffer("A", [[0,1,2], [3,4,5], [6,7,8]])
    >>> B = IntMockBuffer("B", [[0,1,2], [3,4,5], [6,7,8]], shape=(3, 3), strides=(1, 3))
    >>> indirect_strided_and_contig(A, B)
    acquired A
    acquired B
    4
    4
    10
    11
    released A
    released B
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    >>> [str(x) for x in B.recieved_flags]
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    """
    print buf1[1, 1]
    print buf2[1, 1]

    buf1[2, -1] = 10
    buf2[2, -1] = 11

    print buf1[2, 2]
    print buf2[2, 2]


@testcase
def indirect_contig(
             int[::view.indirect_contiguous, ::view.contiguous] buf1,
             int[::view.indirect_contiguous, ::view.generic] buf2):
    """
    >>> A = IntMockBuffer("A", [[0,1,2], [3,4,5], [6,7,8]])
    >>> B = IntMockBuffer("B", [[0,1,2], [3,4,5], [6,7,8]], shape=(3, 3), strides=(1, 3))
    >>> indirect_contig(A, B)
    acquired A
    acquired B
    4
    4
    10
    11
    released A
    released B
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    >>> [str(x) for x in B.recieved_flags]
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    """
    print buf1[1, 1]
    print buf2[1, 1]

    buf1[2, -1] = 10
    buf2[2, -1] = 11

    print buf1[2, 2]
    print buf2[2, 2]



#
# Test compiler options for bounds checking. We create an array with a
# safe "boundary" (memory
# allocated outside of what it published) and then check whether we get back
# what we stored in the memory or an error.

@testcase
def safe_get(int[:] buf, int idx):
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
def unsafe_get(int[:] buf, int idx):
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
def mixed_get(int[:] buf, int unsafe_idx, int safe_idx):
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
# Testing that accessing data using various types of buffer access
# all works.
#

def printbuf_int(int[:] buf, shape):
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
    cdef int[::view.generic, ::view.generic] buf
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
    cdef float[:] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        print buf[i],
    print "END"


#
# Test assignments
#
@testcase
def inplace_operators(int[:] buf):
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
def printbuf_td_cy_int(td_cy_int[:] buf, shape):
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
def printbuf_td_h_short(td_h_short[:] buf, shape):
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
def printbuf_td_h_cy_short(td_h_cy_short[:] buf, shape):
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
def printbuf_td_h_ushort(td_h_ushort[:] buf, shape):
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
def printbuf_td_h_double(td_h_double[:] buf, shape):
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
def printbuf_object(object[:] buf, shape):
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
def assign_to_object(object[:] buf, int idx, obj):
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
def assign_temporary_to_object(object[:] buf):
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
# Test __cythonbufferdefaults__
#
@testcase
def bufdefaults1(int[:] buf):
    """
    For IntStridedMockBuffer, mode should be
    "strided" by defaults which should show
    up in the flags.

    >>> A = IntStridedMockBuffer("A", range(10))
    >>> bufdefaults1(A)
    acquired A
    released A
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'WRITABLE']
    """
    pass


@testcase
def basic_struct(MyStruct[:] buf):
    """
    See also buffmt.pyx

    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="bbqii"))
    1 2 3 4 5
    """
    print buf[0].a, buf[0].b, buf[0].c, buf[0].d, buf[0].e

@testcase
def nested_struct(NestedStruct[:] buf):
    """
    See also buffmt.pyx

    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> nested_struct(NestedStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="T{ii}T{2i}i"))
    1 2 3 4 5
    """
    print buf[0].x.a, buf[0].x.b, buf[0].y.a, buf[0].y.b, buf[0].z

@testcase
def packed_struct(PackedStruct[:] buf):
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
def nested_packed_struct(NestedPackedStruct[:] buf):
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
def complex_dtype(long double complex[:] buf):
    """
    >>> complex_dtype(LongComplexMockBuffer(None, [(0, -1)]))
    -1j
    """
    print buf[0]

@testcase
def complex_inplace(long double complex[:] buf):
    """
    >>> complex_inplace(LongComplexMockBuffer(None, [(0, -1)]))
    (1+1j)
    """
    buf[0] = buf[0] + 1 + 2j
    print buf[0]

@testcase
def complex_struct_dtype(LongComplex[:] buf):
    """
    Note that the format string is "Zg" rather than "2g", yet a struct
    is accessed.
    >>> complex_struct_dtype(LongComplexMockBuffer(None, [(0, -1)]))
    0.0 -1.0
    """
    print buf[0].real, buf[0].imag

@testcase
def complex_struct_inplace(LongComplex[:] buf):
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
    (10, 10)
    """
    cdef int[:] buf = IntMockBuffer(None, [1,2,3])
    cdef int[:] buf2 = IntMockBuffer(None, [4,5,6])

    with nogil:
        buf[1] = 10
        buf2 = buf

    return buf[1], buf2[1]

#
### Test cdef functions
#
class UniqueObject(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

objs = [[UniqueObject("spam")], [UniqueObject("ham")], [UniqueObject("eggs")]]
addref(*[obj for L in objs for obj in L])
cdef cdef_function(int[:] buf1, object[::view.indirect, :] buf2 = ObjectMockBuffer(None, objs)):
    print 'cdef called'
    print buf1[6], buf2[1, 0]
    buf2[1, 0] = UniqueObject("eggs")

@testcase
def test_cdef_function(o1, o2=None):
    """
    >>> A = IntMockBuffer("A", range(10))
    >>> test_cdef_function(A)
    acquired A
    cdef called
    6 ham
    released A
    acquired A
    cdef called
    6 eggs
    released A

    >>> L = [[x] for x in range(25)]
    >>> addref(*[obj for mylist in L for obj in mylist])
    >>> B = ObjectMockBuffer("B", L, shape=(5, 5))

    >>> test_cdef_function(A, B)
    acquired A
    cdef called
    6 eggs
    released A
    acquired A
    cdef called
    6 eggs
    released A
    acquired A
    acquired B
    cdef called
    6 1
    released A
    released B
    """
    cdef_function(o1)
    cdef_function(o1)

    if o2:
        cdef_function(o1, o2)

cdef int[:] global_A = IntMockBuffer("Global_A", range(10))

addref(*[obj for L in objs for obj in L])
cdef object[::view.indirect, :] global_B = ObjectMockBuffer(None, objs)

cdef cdef_function2(int[:] buf1, object[::view.indirect, :] buf2 = global_B):
    print 'cdef2 called'
    print buf1[6], buf2[1, 0]
    buf2[1, 0] = UniqueObject("eggs")

@testcase
def test_cdef_function2():
    """
    >>> test_cdef_function2()
    cdef2 called
    6 ham
    eggs
    cdef2 called
    6 eggs
    """
    cdef int[:] A = global_A
    cdef object[::view.indirect, :] B = global_B

    cdef_function2(A, B)

    del A
    del B

    print global_B[1, 0]

    cdef_function2(global_A, global_B)

@testcase
def test_generic_slicing(arg, indirect=False):
    """
    Test simple slicing
    >>> test_generic_slicing(IntMockBuffer("A", range(8 * 14 * 11), shape=(8, 14, 11)))
    acquired A
    3 9 2
    308 -11 1
    -1 -1 -1
    released A

    Test direct slicing, negative slice oob in dim 2
    >>> test_generic_slicing(IntMockBuffer("A", range(1 * 2 * 3), shape=(1, 2, 3)))
    acquired A
    0 0 2
    12 -3 1
    -1 -1 -1
    released A

    Test indirect slicing
    >>> test_generic_slicing(IntMockBuffer("A", shape_5_3_4_list, shape=(5, 3, 4)), indirect=True)
    acquired A
    2 0 2
    0 1 -1
    released A

    >>> test_generic_slicing(IntMockBuffer("A", shape_9_14_21_list, shape=(9, 14, 21)), indirect=True)
    acquired A
    3 9 2
    10 1 -1
    released A

    """
    cdef int[::view.generic, ::view.generic, :] a = arg
    cdef int[::view.generic, ::view.generic, :] b = a[2:8:2, -4:1:-1, 1:3]

    print b.shape[0], b.shape[1], b.shape[2]

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

@testcase
def test_indirect_slicing(arg):
    """
    Test indirect slicing
    >>> test_indirect_slicing(IntMockBuffer("A", shape_5_3_4_list, shape=(5, 3, 4)))
    acquired A
    5 3 2
    0 0 -1
    58
    56
    released A

    >>> test_indirect_slicing(IntMockBuffer("A", shape_9_14_21_list, shape=(9, 14, 21)))
    acquired A
    5 14 3
    0 16 -1
    2412
    2410
    released A
    """
    cdef int[::view.indirect, ::view.indirect, :] a = arg
    cdef int[::view.indirect, ::view.indirect, :] b = a[-5:, ..., -5:100:2]
    cdef int[::view.indirect, ::view.indirect] c = b[..., 0]

    print b.shape[0], b.shape[1], b.shape[2]
    print b.suboffsets[0] // sizeof(int *),
    print b.suboffsets[1] // sizeof(int),
    print b.suboffsets[2]

    print b[4, 2, 1]
    print c[4, 2]

@testcase
def test_direct_slicing(arg):
    """
    Fused types would be convenient to test this stuff!

    Test simple slicing
    >>> test_direct_slicing(IntMockBuffer("A", range(8 * 14 * 11), shape=(8, 14, 11)))
    acquired A
    3 9 2
    308 -11 1
    -1 -1 -1
    released A

    Test direct slicing, negative slice oob in dim 2
    >>> test_direct_slicing(IntMockBuffer("A", range(1 * 2 * 3), shape=(1, 2, 3)))
    acquired A
    0 0 2
    12 -3 1
    -1 -1 -1
    released A
    """
    cdef int[:, :, ::1] a = arg
    cdef int[:, :, :] b = a[2:8:2, -4:1:-1, 1:3]

    print b.shape[0], b.shape[1], b.shape[2]
    print_int_offsets(b.strides[0], b.strides[1], b.strides[2])
    print_int_offsets(b.suboffsets[0], b.suboffsets[1], b.suboffsets[2])

    cdef int i, j, k
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                itemA = a[2 + 2 * i, -4 - j, 1 + k]
                itemB = b[i, j, k]
                assert itemA == itemB, (i, j, k, itemA, itemB)

@testcase
def test_slicing_and_indexing(arg):
    """
    >>> a = IntStridedMockBuffer("A", range(10 * 3 * 5), shape=(10, 3, 5))
    >>> test_slicing_and_indexing(a)
    acquired A
    5 2
    15 2
    126 113
    [111]
    released A
    """
    cdef int[:, :, :] a = arg
    cdef int[:, :] b = a[-5:, 1, 1::2]
    cdef int[:, :] c = b[4:1:-1, ::-1]
    cdef int[:] d = c[2, 1:2]

    print b.shape[0], b.shape[1]
    print_int_offsets(b.strides[0], b.strides[1])

    cdef int i, j
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            itemA = a[-5 + i, 1, 1 + 2 * j]
            itemB = b[i, j]
            assert itemA == itemB, (i, j, itemA, itemB)

    print c[1, 1], c[2, 0]
    print [d[i] for i in range(d.shape[0])]


@testcase
def test_oob():
    """
    >>> test_oob()
    Traceback (most recent call last):
       ...
    IndexError: Index out of bounds (axis 1)
    """
    cdef int[:, :] a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))
    print a[:, 20]


cdef int nogil_oob(int[:, :] a) nogil except 0:
    a[100, 9:]
    return 1

@testcase
def test_nogil_oob1():
    """
    A is acquired at the beginning of the function and released at the end.
    B is acquired as a temporary and as such is immediately released in the
    except clause.
    >>> test_nogil_oob1()
    acquired A
    acquired B
    released B
    Index out of bounds (axis 0)
    Index out of bounds (axis 0)
    released A
    """
    cdef int[:, :] a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))

    try:
        nogil_oob(IntMockBuffer("B", range(4 * 9), shape=(4, 9)))
    except IndexError, e:
        print e.args[0]

    try:
        with nogil:
            nogil_oob(a)
    except IndexError, e:
        print e.args[0]

@testcase
def test_nogil_oob2():
    """
    >>> test_nogil_oob2()
    Traceback (most recent call last):
       ...
    IndexError: Index out of bounds (axis 0)
    """
    cdef int[:, :] a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))
    with nogil:
        a[100, 9:]

@cython.boundscheck(False)
cdef int cdef_nogil(int[:, :] a) nogil except 0:
    cdef int i, j
    cdef int[:, :] b = a[::-1, 3:10:2]
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            b[i, j] = -b[i, j]

    return 1

@testcase
def test_nogil():
    """
    >>> test_nogil()
    acquired A
    released A
    acquired A
    -25
    released A
    """
    _a = IntMockBuffer("A", range(4 * 9), shape=(4, 9))
    cdef_nogil(_a)
    cdef int[:, :] a = _a
    print a[2, 7]

@testcase
def test_convert_slicenode_to_indexnode():
    """
    When indexing with a[i:j] a SliceNode gets created instead of an IndexNode, which
    forces coercion to object and back. This would not only be inefficient, but it would
    also not compile in nogil mode. So instead we mutate it into an IndexNode.

    >>> test_convert_slicenode_to_indexnode()
    acquired A
    2
    released A
    """
    cdef int[:] a = IntMockBuffer("A", range(10), shape=(10,))
    with nogil:
        a = a[2:4]
    print a[0]

@testcase
@cython.boundscheck(False)
@cython.wraparound(False)
def test_memslice_prange(arg):
    """
    >>> test_memslice_prange(IntMockBuffer("A", range(400), shape=(20, 4, 5)))
    acquired A
    released A
    >>> test_memslice_prange(IntMockBuffer("A", range(200), shape=(100, 2, 1)))
    acquired A
    released A
    """
    cdef int[:, :, :] src, dst

    src = arg

    dst = cython.array((<object> src).shape, sizeof(int), format="i")

    cdef int i, j, k

    for i in prange(src.shape[0], nogil=True):
        for j in range(src.shape[1]):
            for k in range(src.shape[2]):
                dst[i, j, k] = src[i, j, k]

    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            for k in range(src.shape[2]):
                assert src[i, j, k] == dst[i, j, k], (src[i, j, k] == dst[i, j, k])
