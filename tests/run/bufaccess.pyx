# Tests the buffer access syntax functionality by constructing
# mock buffer objects.
#
# Note that the buffers are mock objects created for testing
# the buffer access behaviour -- for instance there is no flag
# checking in the buffer objects (why test our test case?), rather
# what we want to test is what is passed into the flags argument.
#



cimport stdlib
cimport python_buffer
# Add all test_X function docstrings as unit tests

__test__ = {}
setup_string = """
    >>> A = IntMockBuffer("A", range(6))
    >>> B = IntMockBuffer("B", range(6))
    >>> C = IntMockBuffer("C", range(6), (2,3))
    >>> E = ErrorBuffer("E")

"""
    
def testcase(func):
    __test__[func.__name__] = setup_string + func.__doc__
    return func

def testcas(a):
    pass


#
# Buffer acquire and release tests
#

@testcase
def acquire_release(o1, o2):
    """
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
    >>> as_argument(A, 6)
    acquired A
    0 1 2 3 4 5
    released A
    """
    cdef int i
    for i in range(n):
        print bufarg[i],
    print

@testcase
def as_argument_defval(object[int] bufarg=IntMockBuffer('default', range(6)), int n=6):
    """
    >>> as_argument_defval()
    acquired default
    0 1 2 3 4 5
    released default
    >>> as_argument_defval(A, 6)
    acquired A
    0 1 2 3 4 5
    released A
    """
    cdef int i 
    for i in range(n):
        print bufarg[i],
    print

@testcase
def cdef_assignment(obj, n):
    """
    >>> cdef_assignment(A, 6)
    acquired A
    0 1 2 3 4 5
    released A
    
    """
    cdef object[int] buf = obj
    cdef int i
    for i in range(n):
        print buf[i],
    print

@testcase
def forin_assignment(objs, int pick):
    """
    >>> as_argument_defval()
    acquired default
    0 1 2 3 4 5
    released default
    >>> as_argument_defval(A, 6)
    acquired A
    0 1 2 3 4 5
    released A
    """
    cdef object[int] buf
    for buf in objs:
        print buf[pick]

@testcase
def cascaded_buffer_assignment(obj):
    """
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
# Index bounds checking
# 
@testcase
def get_int_2d(object[int, 2] buf, int i, int j):
    """
    Check negative indexing:
    >>> get_int_2d(C, 1, 1)
    acquired C
    released C
    4
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
def get_int_2d_uintindex(object[int, 2] buf, unsigned int i, unsigned int j):
    """
    Unsigned indexing:
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


#
# Buffer type mismatch examples. Varying the type and access
# method simultaneously, the odds of an interaction is virtually
# zero.
#
@testcase
def fmtst1(buf):
    """
    >>> fmtst1(IntMockBuffer("A", range(3)))
    Traceback (most recent call last):
        ...
    ValueError: Buffer datatype mismatch (rejecting on 'i')
    """
    cdef object[float] a = buf

@testcase
def fmtst2(object[int] buf):
    """
    >>> fmtst2(FloatMockBuffer("A", range(3)))
    Traceback (most recent call last):
        ...
    ValueError: Buffer datatype mismatch (rejecting on 'f')
    """

@testcase
def ndim1(object[int, 2] buf):
    """
    >>> ndim1(IntMockBuffer("A", range(3)))
    Traceback (most recent call last):
        ...
    ValueError: Buffer has wrong number of dimensions (expected 2, got 1)
    """

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
    >>> R.recieved_flags
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES']
    """
    cdef object[unsigned short int, 3] buf = obj
    print buf[2, 2, 1]

@testcase
def writable(obj):
    """
    >>> R = UnsignedShortMockBuffer("R", range(27), shape=(3, 3, 3))
    >>> writable(R)
    acquired R
    released R
    >>> R.recieved_flags
    ['FORMAT', 'INDIRECT', 'ND', 'STRIDES', 'WRITABLE']
    """
    cdef object[unsigned short int, 3] buf = obj
    buf[2, 2, 1] = 23


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


#
# Testing that accessing data using various types of buffer access
# all works.
#


@testcase
def printbuf_int_2d(o, shape):
    """
    Strided:
    
    >>> printbuf_int_2d(IntMockBuffer("A", range(6), (2,3)), (2,3))
    acquired A
    0 1 2
    3 4 5
    released A
    >>> printbuf_int_2d(IntMockBuffer("A", range(100), (3,3), strides=(20,5)), (3,3))
    acquired A
    0 5 10
    20 25 30
    40 45 50
    released A

    Indirect:
    >>> printbuf_int_2d(IntMockBuffer("A", [[1,2],[3,4]]), (2,2))
    acquired A
    1 2
    3 4
    released A
    """
    # should make shape builtin
    cdef object[int, 2] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        for j in range(shape[1]):
            print buf[i, j],
        print

@testcase
def printbuf_float(o, shape):
    """
    >>> printbuf_float(FloatMockBuffer("F", [1.0, 1.25, 0.75, 1.0]), (4,))
    acquired F
    1.0 1.25 0.75 1.0
    released F
    """

    # should make shape builtin
    cdef object[float] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        print buf[i],
    print


available_flags = (
    ('FORMAT', python_buffer.PyBUF_FORMAT),
    ('INDIRECT', python_buffer.PyBUF_INDIRECT),
    ('ND', python_buffer.PyBUF_ND),
    ('STRIDES', python_buffer.PyBUF_STRIDES),
    ('WRITABLE', python_buffer.PyBUF_WRITABLE)
)

cimport stdio

cdef class MockBuffer:
    cdef object format
    cdef void* buffer
    cdef int len, itemsize, ndim
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    cdef Py_ssize_t* suboffsets
    cdef object label, log
    
    cdef readonly object recieved_flags
    cdef public object fail
    
    def __init__(self, label, data, shape=None, strides=None, format=None):
        self.label = label
        self.log = ""
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
            #  printf("%ld; %ld %ld %ld %ld %ld", i0, s0, o0, i1, s1, o1);

        else:
            # strided and/or simple access
            self.buffer = self.create_buffer(data)
            self.ndim = len(shape)
            self.suboffsets = NULL
            
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
        
        if buffer is NULL:
            print u"locking!"
            return

        self.recieved_flags = []
        cdef int value
        for name, value in available_flags:
            if (value & flags) == value:
                self.recieved_flags.append(name)
        
        buffer.buf = self.buffer
        buffer.len = self.len
        buffer.readonly = 0
        buffer.format = <char*>self.format
        buffer.ndim = self.ndim
        buffer.shape = self.shape
        buffer.strides = self.strides
        buffer.suboffsets = self.suboffsets
        buffer.itemsize = self.itemsize
        buffer.internal = NULL
        msg = "acquired %s" % self.label
        print msg
        self.log += msg + "\n"

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        msg = "released %s" % self.label
        print msg 
        self.log += msg + "\n"

    def printlog(self):
        print self.log,

    def resetlog(self):
        self.log = ""

    cdef int write(self, char* buf, object value) except -1: raise Exception()
    cdef get_itemsize(self):
        print "ERROR, not subclassed", self.__class__
    cdef get_default_format(self):
        print "ERROR, not subclassed", self.__class__
    
cdef class FloatMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<float*>buf)[0] = <float>value
        return 0
    cdef get_itemsize(self): return sizeof(float)
    cdef get_default_format(self): return "=f"

cdef class IntMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<int*>buf)[0] = <int>value
        return 0
    cdef get_itemsize(self): return sizeof(int)
    cdef get_default_format(self): return "=i"

cdef class UnsignedShortMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<unsigned short*>buf)[0] = <unsigned short>value
        return 0
    cdef get_itemsize(self): return sizeof(unsigned short)
    cdef get_default_format(self): return "=H"
            
cdef class ErrorBuffer:
    cdef object label
    
    def __init__(self, label):
        self.label = label

    def __getbuffer__(MockBuffer self, Py_buffer* buffer, int flags):
        raise Exception("acquiring %s" % self.label)

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        raise Exception("releasing %s" % self.label)

