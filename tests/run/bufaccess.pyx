cimport __cython__

__doc__ = u"""
    >>> A = MockBuffer("i", range(10), label="A")
    >>> B = MockBuffer("i", range(10), label="B")
    >>> E = ErrorBuffer("E")
    
    >>> acquire_release(A, B)
    acquired A
    released A
    acquired B
    released B

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

    >>> as_argument(MockBuffer("i", range(6)), 6)
    acquired
    0 1 2 3 4 5
    released
    >>> as_argument_defval()
    acquired
    0 1 2 3 4 5
    released
    >>> as_argument_defval(MockBuffer("i", range(6)), 6)
    acquired
    0 1 2 3 4 5
    released

    >>> cdef_assignment(A, 6)
    acquired A
    0 1 2 3 4 5
    released A

    #>>> forin_assignment([A, B, A], 3)
    acquired A
    3
    released A
    acquired B
    3
    released B
    acquired A
    3
    released A   
    
    >>> printbuf_float(MockBuffer("f", [1.0, 1.25, 0.75, 1.0]), (4,))
    acquired
    1.0 1.25 0.75 1.0
    released
    
    >>> printbuf_int_2d(MockBuffer("i", range(6), (2,3)), (2,3))
    acquired
    0 1 2
    3 4 5
    released
"""

ctypedef char* (*write_func_ptr)(char*, object)
cdef char* write_float(char* buf, object value):
    (<float*>buf)[0] = <float>value
    return buf + sizeof(float)
cdef char* write_int(char* buf, object value):
    (<int*>buf)[0] = <int>value
    return buf + sizeof(int)

# long can hold  a pointer on all target platforms,
# though really we should have a seperate typedef for this..
# TODO: Should create subclasses of MockBuffer instead.
typemap = {
    'f': (sizeof(float), <unsigned long>&write_float),
    'i': (sizeof(int), <unsigned long>&write_int)
}
 
cimport stdlib

def acquire_release(o1, o2):
    cdef object[int] buf
    buf = o1
    buf = o2

def acquire_raise(o):
    cdef object[int] buf
    buf = o
    raise Exception("on purpose")

def as_argument(object[int] bufarg, int n):
    cdef int i
    for i in range(n):
        print bufarg[i],
    print

def as_argument_defval(object[int] bufarg=MockBuffer('i', range(6)), int n=6):
    cdef int i 
    for i in range(n):
        print bufarg[i],
    print

def cdef_assignment(obj, n):
    cdef object[int] buf = obj
    cdef int i
    for i in range(n):
        print buf[i],
    print

def forin_assignment(objs, int pick):
    cdef object[int] buf
    for buf in objs:
        print buf[pick]

def printbuf_float(o, shape):
    # should make shape builtin
    cdef object[float] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        print buf[i],
    print
 

def printbuf_int_2d(o, shape):
    # should make shape builtin
    cdef object[int, 2] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        for j in range(shape[1]):
            print buf[i, j],
        print
 
cdef class MockBuffer:
    cdef object format
    cdef char* buffer
    cdef int len, itemsize, ndim
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    cdef write_func_ptr wfunc
    cdef object label, log
    
    def __init__(self, typechar, data, shape=None, strides=None, format=None, label=None):
        self.label = label
        self.log = ""
        if format is None: format = "=%s" % typechar
        self.itemsize, x = typemap[typechar]
        self.wfunc = <write_func_ptr><unsigned long>x
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
        self.fill_buffer(typechar, data)
        self.ndim = len(shape)
        self.strides = <Py_ssize_t*>stdlib.malloc(self.ndim * sizeof(Py_ssize_t))
        for i, x in enumerate(strides):
            self.strides[i] = x
        self.shape = <Py_ssize_t*>stdlib.malloc(self.ndim * sizeof(Py_ssize_t))

    def __getbuffer__(MockBuffer self, Py_buffer* buffer, int flags):
        global log
        if buffer is NULL:
            print u"locking!"
            return
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
        msg = "acquired"
        if self.label: msg += " " + self.label
        print msg
        self.log += msg + "\n"

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        global log
        msg = "released"
        if self.label: msg += " " + self.label
        print msg
        self.log += msg + "\n"
        
    cdef fill_buffer(self, typechar, object data):
        cdef char* it = self.buffer
        for value in data:
            it = self.wfunc(it, value)

    def printlog(self):
        print self.log,

    def resetlog(self):
        self.log = ""
            
cdef class ErrorBuffer:
    cdef object label
    
    def __init__(self, label):
        self.label = label

    def __getbuffer__(MockBuffer self, Py_buffer* buffer, int flags):
        raise Exception("acquiring %s" % self.label)

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        raise Exception("releasing %s" % self.label)
