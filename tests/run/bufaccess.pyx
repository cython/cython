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

@testcase
def acquire_release(o1, o2):
    """
    >>> acquire_release(A, B)
    acquired A
    released A
    acquired B
    released B
    """
    cdef object[int] buf
    buf = o1
    buf = o2

#@testcase
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
    o.printlog()
    raise Exception("on purpose")

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
def printbuf_int_2d(o, shape):
    """
    >>> printbuf_int_2d(C, (2,3))
    acquired C
    0 1 2
    3 4 5
    released C
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

cdef class MockBuffer:
    cdef object format
    cdef char* buffer
    cdef int len, itemsize, ndim
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    cdef object label, log
    cdef readonly object recieved_flags
    
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
        self.format = format
        self.len = len(data) * self.itemsize
        self.buffer = <char*>stdlib.malloc(self.len)
        self.fill_buffer(data)
        self.ndim = len(shape)
        self.strides = <Py_ssize_t*>stdlib.malloc(self.ndim * sizeof(Py_ssize_t))
        for i, x in enumerate(strides):
            self.strides[i] = x
        self.shape = <Py_ssize_t*>stdlib.malloc(self.ndim * sizeof(Py_ssize_t))
        for i, x in enumerate(shape):
            self.shape[i] = x
    def __dealloc__(self):
        stdlib.free(self.strides)
        stdlib.free(self.shape)
        
    def __getbuffer__(MockBuffer self, Py_buffer* buffer, int flags):
        if buffer is NULL:
            print u"locking!"
            return

        self.recieved_flags = []
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
        buffer.suboffsets = NULL
        buffer.itemsize = self.itemsize
        buffer.internal = NULL
        msg = "acquired %s" % self.label
        print msg
        self.log += msg + "\n"

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        msg = "released %s" % self.label
        print msg
        self.log += msg + "\n"
        
    cdef fill_buffer(self, object data):
        cdef char* it = self.buffer
        for value in data:
            self.write(it, value)
            it += self.itemsize

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

