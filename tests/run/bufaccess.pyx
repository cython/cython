# Tests the buffer access syntax functionality by constructing
# mock buffer objects.
#
# Note that the buffers are mock objects created for testing
# the buffer access behaviour -- for instance there is no flag
# checking in the buffer objects (why test our test case?), rather
# what we want to test is what is passed into the flags argument.
#

from __future__ import unicode_literals

cimport stdlib
cimport python_buffer
cimport stdio
cimport cython

from python_ref cimport PyObject

__test__ = {}

import re
exclude = []#re.compile('object').search]
    
def testcase(func):
    for e in exclude:
        if e(func.__name__):
            return func
    __test__[func.__name__] = func.__doc__
    return func

def testcas(a):
    pass


#
# Buffer acquire and release tests
#

def nousage():
    """
    The challenge here is just compilation.
    """
    cdef object[int, ndim=2] buf

def printbuf():
    """
    Just compilation.
    """
    cdef object[int, ndim=2] buf
    print buf

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
    TypeError: 'int' does not have the buffer interface
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
    >>> [str(x) for x in R.recieved_flags]  # Works in both py2 and py3
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
    >>> [str(x) for x in R.recieved_flags] # Py2/3
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
    >>> [str(x) for x in A.recieved_flags] # Py2/3
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
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'C_CONTIGUOUS']
    """
    return buf[2]
    
@testcase
def c_contig_2d(object[int, ndim=2, mode='c'] buf):
    """
    Multi-dim has seperate implementation
    
    >>> A = IntMockBuffer(None, range(12), shape=(3,4))
    >>> c_contig_2d(A)
    7
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES', 'C_CONTIGUOUS']
    """
    return buf[1, 3]

@testcase
def f_contig(object[int, ndim=1, mode='fortran'] buf):
    """
    >>> A = IntMockBuffer(None, range(4))
    >>> f_contig(A)
    2
    >>> [str(x) for x in A.recieved_flags]
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
    >>> [str(x) for x in A.recieved_flags]
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
@testcase
def coercions(object[unsigned char] uc):
    """
TODO    
    """
    print type(uc[0])
    uc[0] = -1
    print uc[0]
    uc[0] = <int>3.14
    print uc[0]

    cdef char* ch = b"asfd"
    cdef object[object] objbuf
    objbuf[3] = ch


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
    ValueError: Buffer dtype mismatch, expected 'bufaccess.td_cy_int' but got 'short'
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
    ValueError: Buffer dtype mismatch, expected 'bufaccess.td_h_short' but got 'int'
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
    ValueError: Buffer dtype mismatch, expected 'bufaccess.td_h_cy_short' but got 'int'
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
    ValueError: Buffer dtype mismatch, expected 'bufaccess.td_h_ushort' but got 'short'
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
    ValueError: Buffer dtype mismatch, expected 'bufaccess.td_h_double' but got 'float'
    """
    cdef int i
    for i in range(shape[0]):
        print buf[i],
    print 'END'


#
# Object access
#
from python_ref cimport Py_INCREF, Py_DECREF
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
# Testcase support code (more tests below!, because of scope rules)
#


available_flags = (
    ('FORMAT', python_buffer.PyBUF_FORMAT),
    ('INDIRECT', python_buffer.PyBUF_INDIRECT),
    ('ND', python_buffer.PyBUF_ND),
    ('STRIDES', python_buffer.PyBUF_STRIDES),
    ('C_CONTIGUOUS', python_buffer.PyBUF_C_CONTIGUOUS),
    ('F_CONTIGUOUS', python_buffer.PyBUF_F_CONTIGUOUS),
    ('WRITABLE', python_buffer.PyBUF_WRITABLE)
)

cdef class MockBuffer:
    cdef object format, offset
    cdef void* buffer
    cdef int len, itemsize, ndim
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    cdef Py_ssize_t* suboffsets
    cdef object label, log
    
    cdef readonly object recieved_flags, release_ok
    cdef public object fail
    
    def __init__(self, label, data, shape=None, strides=None, format=None, offset=0):
        # It is important not to store references to data after the constructor
        # as refcounting is checked on object buffers.
        self.label = label
        self.release_ok = True
        self.log = ""
        self.offset = offset
        self.itemsize = self.get_itemsize()
        if format is None: format = self.get_default_format()
        if shape is None: shape = (len(data),)
        if strides is None:
            strides = []
            cumprod = 1
            rshape = list(shape)
            rshape.reverse()
            for s in rshape:
                strides.append(cumprod)
                cumprod *= s
            strides.reverse()
        strides = [x * self.itemsize for x in strides]
        suboffsets = [-1] * len(shape)
        datashape = [len(data)]
        p = data
        while True:
            p = p[0]
            if isinstance(p, list): datashape.append(len(p))
            else: break
        if len(datashape) > 1:
            # indirect access
            self.ndim = len(datashape)
            shape = datashape
            self.buffer = self.create_indirect_buffer(data, shape)
            suboffsets = [0] * (self.ndim-1) + [-1]
            strides = [sizeof(void*)] * (self.ndim-1) + [self.itemsize]
            self.suboffsets = self.list_to_sizebuf(suboffsets)
        else:
            # strided and/or simple access
            self.buffer = self.create_buffer(data)
            self.ndim = len(shape)
            self.suboffsets = NULL

        try:
            format = format.encode('ASCII')
        except AttributeError:
            pass
        self.format = format
        self.len = len(data) * self.itemsize

        self.strides = self.list_to_sizebuf(strides)
        self.shape = self.list_to_sizebuf(shape)
            
    def __dealloc__(self):
        stdlib.free(self.strides)
        stdlib.free(self.shape)
        if self.suboffsets != NULL:
            stdlib.free(self.suboffsets)
            # must recursively free indirect...
        else:
            stdlib.free(self.buffer)
    
    cdef void* create_buffer(self, data):
        cdef char* buf = <char*>stdlib.malloc(len(data) * self.itemsize)
        cdef char* it = buf
        for value in data:
            self.write(it, value)
            it += self.itemsize
        return buf

    cdef void* create_indirect_buffer(self, data, shape):
        cdef void** buf
        assert shape[0] == len(data)
        if len(shape) == 1:
            return self.create_buffer(data)
        else:
            shape = shape[1:]
            buf = <void**>stdlib.malloc(len(data) * sizeof(void*))
            for idx, subdata in enumerate(data):
                buf[idx] = self.create_indirect_buffer(subdata, shape)
            return buf

    cdef Py_ssize_t* list_to_sizebuf(self, l):
        cdef Py_ssize_t* buf = <Py_ssize_t*>stdlib.malloc(len(l) * sizeof(Py_ssize_t))
        for i, x in enumerate(l):
            buf[i] = x
        return buf

    def __getbuffer__(MockBuffer self, Py_buffer* buffer, int flags):
        if self.fail:
            raise ValueError("Failing on purpose")

        self.recieved_flags = []
        cdef int value
        for name, value in available_flags:
            if (value & flags) == value:
                self.recieved_flags.append(name)
        
        buffer.buf = <void*>(<char*>self.buffer + (<int>self.offset * self.itemsize))
        buffer.obj = self
        buffer.len = self.len
        buffer.readonly = 0
        buffer.format = <char*>self.format
        buffer.ndim = self.ndim
        buffer.shape = self.shape
        buffer.strides = self.strides
        buffer.suboffsets = self.suboffsets
        buffer.itemsize = self.itemsize
        buffer.internal = NULL
        if self.label:
            msg = "acquired %s" % self.label
            print msg
            self.log += msg + "\n"

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        if buffer.suboffsets != self.suboffsets:
            self.release_ok = False
        if self.label:
            msg = "released %s" % self.label
            print msg 
            self.log += msg + "\n"

    def printlog(self):
        print self.log[:-1]

    def resetlog(self):
        self.log = ""

    cdef int write(self, char* buf, object value) except -1: raise Exception()
    cdef get_itemsize(self):
        print "ERROR, not subclassed", self.__class__
    cdef get_default_format(self):
        print "ERROR, not subclassed", self.__class__
    
cdef class CharMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<char*>buf)[0] = <int>value
        return 0
    cdef get_itemsize(self): return sizeof(char)
    cdef get_default_format(self): return b"@b"

cdef class IntMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<int*>buf)[0] = <int>value
        return 0
    cdef get_itemsize(self): return sizeof(int)
    cdef get_default_format(self): return b"@i"

cdef class UnsignedIntMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<unsigned int*>buf)[0] = <unsigned int>value
        return 0
    cdef get_itemsize(self): return sizeof(unsigned int)
    cdef get_default_format(self): return b"@I"

cdef class ShortMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<short*>buf)[0] = <short>value
        return 0
    cdef get_itemsize(self): return sizeof(short)
    cdef get_default_format(self): return b"h" # Try without endian specifier

cdef class UnsignedShortMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<unsigned short*>buf)[0] = <unsigned short>value
        return 0
    cdef get_itemsize(self): return sizeof(unsigned short)
    cdef get_default_format(self): return b"@1H" # Try with repeat count

cdef class FloatMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<float*>buf)[0] = <float>value
        return 0
    cdef get_itemsize(self): return sizeof(float)
    cdef get_default_format(self): return b"f"

cdef class DoubleMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<double*>buf)[0] = <double>value
        return 0
    cdef get_itemsize(self): return sizeof(double)
    cdef get_default_format(self): return b"d"

cdef extern from *:
    void* addr_of_pyobject "(void*)"(object)

cdef class ObjectMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<void**>buf)[0] = addr_of_pyobject(value)
        return 0

    cdef get_itemsize(self): return sizeof(void*)
    cdef get_default_format(self): return b"@O"
        

cdef class IntStridedMockBuffer(IntMockBuffer):
    cdef __cythonbufferdefaults__ = {"mode" : "strided"}
            
cdef class ErrorBuffer:
    cdef object label
    
    def __init__(self, label):
        self.label = label

    def __getbuffer__(ErrorBuffer self, Py_buffer* buffer, int flags):
        raise Exception("acquiring %s" % self.label)

    def __releasebuffer__(ErrorBuffer self, Py_buffer* buffer):
        raise Exception("releasing %s" % self.label)

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
    >>> [str(x) for x in A.recieved_flags]
    ['FORMAT', 'ND', 'STRIDES']
    """
    pass
    

#
# Structs
#
cdef struct MyStruct:
    char a
    char b
    long long int c
    int d
    int e

cdef struct SmallStruct:
    int a
    int b

cdef struct NestedStruct:
    SmallStruct x
    SmallStruct y
    int z

cdef class MyStructMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef MyStruct* s
        s = <MyStruct*>buf;
        s.a, s.b, s.c, s.d, s.e = value
        return 0
    
    cdef get_itemsize(self): return sizeof(MyStruct)
    cdef get_default_format(self): return b"2bq2i"

cdef class NestedStructMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef NestedStruct* s
        s = <NestedStruct*>buf;
        s.x.a, s.x.b, s.y.a, s.y.b, s.z = value
        return 0
    
    cdef get_itemsize(self): return sizeof(NestedStruct)
    cdef get_default_format(self): return b"2T{ii}i"

@testcase
def basic_struct(object[MyStruct] buf):
    """
    See also buffmt.pyx
    
    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)]))
    1 2 3 4 5
    >>> basic_struct(MyStructMockBuffer(None, [(1, 2, 3, 4, 5)], format="bbqii"))
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

cdef struct LongComplex:
    long double real
    long double imag

cdef class LongComplexMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef LongComplex* s
        s = <LongComplex*>buf;
        s.real, s.imag = value
        return 0
    
    cdef get_itemsize(self): return sizeof(LongComplex)
    cdef get_default_format(self): return b"Zg"

#cdef extern from "complex.h":
#    pass

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
    
