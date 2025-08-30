cimport cpython.buffer
cimport cpython.mem as pymem

import sys

available_flags = (
    ('FORMAT', cpython.buffer.PyBUF_FORMAT),
    ('INDIRECT', cpython.buffer.PyBUF_INDIRECT),
    ('ND', cpython.buffer.PyBUF_ND),
    ('STRIDES', cpython.buffer.PyBUF_STRIDES),
    ('C_CONTIGUOUS', cpython.buffer.PyBUF_C_CONTIGUOUS),
    ('F_CONTIGUOUS', cpython.buffer.PyBUF_F_CONTIGUOUS),
    ('WRITABLE', cpython.buffer.PyBUF_WRITABLE)
)

cdef class MockBuffer:
    cdef object format, offset
    cdef void* buffer
    cdef Py_ssize_t len, itemsize
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    cdef Py_ssize_t* suboffsets
    cdef object label, log
    cdef int ndim
    cdef bint writable

    cdef readonly object received_flags, release_ok
    cdef public object fail

    def __init__(self, label, data, shape=None, strides=None, format=None, writable=True, offset=0):
        # It is important not to store references to data after the constructor
        # as refcounting is checked on object buffers.
        cdef Py_ssize_t x, s, cumprod, itemsize
        self.label = label
        self.release_ok = True
        self.log = u""
        self.offset = offset
        self.itemsize = itemsize = self.get_itemsize()
        self.writable = writable
        if format is None: format = self.get_default_format()
        if shape is None: shape = (len(data),)
        if strides is None:
            strides = []
            cumprod = 1
            for s in shape[::-1]:
                strides.append(cumprod)
                cumprod *= s
            strides.reverse()
        strides = [x * itemsize for x in strides]
        suboffsets = [-1] * len(shape)
        datashape = [len(data)]
        p = data
        while True:
            p = p[0]
            if isinstance(p, list): datashape.append(len(p))
            else: break
        if len(datashape) > 1:
            # indirect access
            self.ndim = <int>len(datashape)
            shape = datashape
            self.buffer = self.create_indirect_buffer(data, shape)
            suboffsets = [0] * self.ndim
            suboffsets[-1] = -1
            strides = [sizeof(void*)] * self.ndim
            strides[-1] = itemsize
            self.suboffsets = self.list_to_sizebuf(suboffsets)
        else:
            # strided and/or simple access
            self.buffer = self.create_buffer(data)
            self.ndim = <int>len(shape)
            self.suboffsets = NULL

        try:
            format = format.encode('ASCII')
        except AttributeError:
            pass
        self.format = format
        self.len = len(data) * itemsize

        self.strides = self.list_to_sizebuf(strides)
        self.shape = self.list_to_sizebuf(shape)

    def __dealloc__(self):
        pymem.PyMem_Free(self.strides)
        pymem.PyMem_Free(self.shape)
        if self.suboffsets != NULL:
            pymem.PyMem_Free(self.suboffsets)
            # must recursively free indirect...
        else:
            pymem.PyMem_Free(self.buffer)

    cdef void* create_buffer(self, data) except NULL:
        cdef size_t n = <size_t>(len(data) * self.itemsize)
        cdef char* buf = <char*>pymem.PyMem_Malloc(n)
        if buf == NULL:
            raise MemoryError
        cdef char* it = buf
        for value in data:
            self.write(it, value)
            it += self.itemsize
        return buf

    cdef void* create_indirect_buffer(self, data, shape) except NULL:
        cdef size_t n = 0
        cdef void** buf
        assert shape[0] == len(data), (shape[0], len(data))
        if len(shape) == 1:
            return self.create_buffer(data)
        else:
            shape = shape[1:]
            n = <size_t>len(data) * sizeof(void*)
            buf = <void**>pymem.PyMem_Malloc(n)
            if buf == NULL:
                return NULL

            for idx, subdata in enumerate(data):
                buf[idx] = self.create_indirect_buffer(subdata, shape)

            return buf

    cdef Py_ssize_t* list_to_sizebuf(self, l):
        cdef Py_ssize_t i, x
        cdef size_t n = <size_t>len(l) * sizeof(Py_ssize_t)
        cdef Py_ssize_t* buf = <Py_ssize_t*>pymem.PyMem_Malloc(n)
        for i, x in enumerate(l):
            buf[i] = x
        return buf

    def __getbuffer__(MockBuffer self, Py_buffer* buffer, int flags):
        if self.fail:
            raise ValueError("Failing on purpose")

        cdef int value
        self.received_flags = [
            name for name, value in available_flags
            if (value & flags) == value
        ]

        if flags & cpython.buffer.PyBUF_WRITABLE and not self.writable:
            raise BufferError(f"Writable buffer requested from read-only mock: {' | '.join(self.received_flags)}")

        buffer.buf = <void*>(<char*>self.buffer + (<int>self.offset * self.itemsize))
        buffer.obj = self
        buffer.len = self.len
        buffer.readonly = not self.writable
        buffer.format = <char*>self.format
        buffer.ndim = self.ndim
        buffer.shape = self.shape
        buffer.strides = self.strides
        buffer.suboffsets = self.suboffsets
        buffer.itemsize = self.itemsize
        buffer.internal = NULL
        if self.label:
            msg = f"acquired {self.label}"
            print(msg)
            self.log += msg + u"\n"

    def __releasebuffer__(MockBuffer self, Py_buffer* buffer):
        if buffer.suboffsets != self.suboffsets:
            self.release_ok = False
        if self.label:
            msg = f"released {self.label}"
            print(msg)
            self.log += msg + u"\n"

    def printlog(self):
        print(self.log[:-1])

    def resetlog(self):
        self.log = u""

    cdef int write(self, char* buf, object value) except -1: raise Exception()
    cdef get_itemsize(self):
        print(f"ERROR, not subclassed: {self.__class__}")
    cdef get_default_format(self):
        print(f"ERROR, not subclassed {self.__class__}")

cdef class CharMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        (<char*>buf)[0] = <char>value
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
        (<float*>buf)[0] = <float>(<double>value)
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
        raise Exception(f"acquiring {self.label}")

    def __releasebuffer__(ErrorBuffer self, Py_buffer* buffer):
        raise Exception(f"releasing {self.label}")

#
# Structs
#
cdef struct MyStruct:
    signed char a
    signed char b
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

cdef packed struct PackedStruct:
    signed char a
    int b

cdef struct NestedPackedStruct:
    signed char a
    int b
    PackedStruct sub
    int c

cdef class MyStructMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef MyStruct* s
        s = <MyStruct*>buf
        s.a, s.b, s.c, s.d, s.e = value
        return 0

    cdef get_itemsize(self): return sizeof(MyStruct)
    cdef get_default_format(self): return b"2cq2i"

cdef class NestedStructMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef NestedStruct* s
        s = <NestedStruct*>buf
        s.x.a, s.x.b, s.y.a, s.y.b, s.z = value
        return 0

    cdef get_itemsize(self): return sizeof(NestedStruct)
    cdef get_default_format(self): return b"2T{ii}i"

cdef class PackedStructMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef PackedStruct* s
        s = <PackedStruct*>buf
        s.a, s.b = value
        return 0

    cdef get_itemsize(self): return sizeof(PackedStruct)
    cdef get_default_format(self): return b"^ci"

cdef class NestedPackedStructMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef NestedPackedStruct* s
        s = <NestedPackedStruct*>buf
        s.a, s.b, s.sub.a, s.sub.b, s.c = value
        return 0

    cdef get_itemsize(self): return sizeof(NestedPackedStruct)
    cdef get_default_format(self): return b"ci^ci@i"

cdef struct LongComplex:
    long double real
    long double imag

cdef class LongComplexMockBuffer(MockBuffer):
    cdef int write(self, char* buf, object value) except -1:
        cdef LongComplex* s
        s = <LongComplex*>buf
        s.real, s.imag = value
        return 0

    cdef get_itemsize(self): return sizeof(LongComplex)
    cdef get_default_format(self): return b"Zg"


def print_offsets(*args, size, newline=True):
    sys.stdout.write(' '.join([str(item // size) for item in args]) + ('\n' if newline else ''))

def print_int_offsets(*args, newline=True):
    print_offsets(*args, size=sizeof(int), newline=newline)


shape_5_3_4_list = [[list(range(k * 12 + j * 4, k * 12 + j * 4 + 4))
                        for j in range(3)]
                            for k in range(5)]

stride1 = 21 * 14
stride2 = 21
shape_9_14_21_list = [[list(range(k * stride1 + j * stride2, k * stride1 + j * stride2 + 21))
                           for j in range(14)]
                               for k in range(9)]
