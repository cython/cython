cimport __cython__

__doc__ = u"""
    >>> fb = MockBuffer("=f", "f", [1.0, 1.25, 0.75, 1.0], (2,2))
    >>> printbuf_float(fb, (2,2))
    1.0 1.25
    0.75 1.0
"""


def printbuf_float(o, shape):
    # should make shape builtin
    cdef object[float, 2] buf
    buf = o
    cdef int i, j
    for i in range(shape[0]):
        for j in range(shape[1]):
            print buf[i, j],
        print
 


sizes = {
    'f': sizeof(float)
} 
 
cimport stdlib

cdef class MockBuffer:
    cdef object format
    cdef char* buffer
    cdef int len, itemsize, ndim
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    
    def __init__(self, format, typechar, data, shape=None, strides=None):
        self.itemsize = sizes[typechar]
        if shape is None: shape = (len(data),)
        if strides is None:
            strides = []
            cumprod = 1
            for s in shape:
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
        
    cdef fill_buffer(self, typechar, object data):
        cdef int idx = 0
        for value in data:
            (<float*>(self.buffer + idx))[0] = <float>value
            idx += sizeof(float)
            
            
