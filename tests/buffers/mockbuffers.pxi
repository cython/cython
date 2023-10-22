from libc cimport stdlib
cimport cpython.buffer

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
    cdef isize len, itemsize
    cdef Py_ssize_t* strides
    cdef Py_ssize_t* shape
    cdef Py_ssize_t* suboffsets
    cdef object label, log
    cdef i32 ndim
    cdef bint writable

    cdef readonly object received_flags, release_ok
    pub object fail

    def __init__(self, label, data, shape=None, strides=None, format=None, writable=true, offset=0):
        # It is important not to store references to data after the constructor
        # as refcounting is checked on object buffers.
        cdef isize x, s, cumprod, itemsize
        self.label = label
        self.release_ok = true
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
        while true:
            p = p[0]
            if isinstance(p, list): datashape.append(len(p))
            else: break
        if len(datashape) > 1:
            # indirect access
            self.ndim = <i32>len(datashape)
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
            self.ndim = <i32>len(shape)
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
        stdlib.free(self.strides)
        stdlib.free(self.shape)
        if self.suboffsets != NULL:
            stdlib.free(self.suboffsets)
            # must recursively free indirect...
        else:
            stdlib.free(self.buffer)

    cdef void* create_buffer(self, data) except NULL:
        cdef usize n = <usize>(len(data) * self.itemsize)
        cdef char* buf = <char*>stdlib.malloc(n)
        if buf == NULL:
            raise MemoryError
        cdef char* it = buf
        for value in data:
            self.write(it, value)
            it += self.itemsize
        return buf

    cdef void* create_indirect_buffer(self, data, shape) except NULL:
        cdef usize n = 0
        cdef void** buf
        assert shape[0] == len(data), (shape[0], len(data))
        if len(shape) == 1:
            return self.create_buffer(data)
        else:
            shape = shape[1:]
            n = <usize>len(data) * sizeof(void*)
            buf = <void**>stdlib.malloc(n)
            if buf == NULL:
                return NULL

            for idx, subdata in enumerate(data):
                buf[idx] = self.create_indirect_buffer(subdata, shape)

            return buf

    cdef isize* list_to_sizebuf(self, l):
        cdef isize i, x
        cdef usize n = <usize>len(l) * sizeof(isize)
        cdef isize* buf = <isize*>stdlib.malloc(n)
        for i, x in enumerate(l):
            buf[i] = x
        return buf

    def __getbuffer__(MockBuffer self, Py_buffer* buffer, i32 flags):
        if self.fail:
            raise ValueError("Failing on purpose")

        self.received_flags = []
        cdef i32 value
        for name, value in available_flags:
            if (value & flags) == value:
                self.received_flags.append(name)

        if flags & cpython.buffer.PyBUF_WRITABLE and not self.writable:
            raise BufferError(f"Writable buffer requested from read-only mock: {' | '.join(self.received_flags)}")

        buffer.buf = <void*>(<char*>self.buffer + (<i32>self.offset * self.itemsize))
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
            self.release_ok = false
        if self.label:
            msg = f"released {self.label}"
            print(msg)
            self.log += msg + u"\n"

    def printlog(self):
        print(self.log[:-1])

    def resetlog(self):
        self.log = u""

    cdef i32 write(self, char* buf, object value) except -1: raise Exception()
    cdef get_itemsize(self):
        print(f"ERROR, not subclassed: {self.__class__}")
    cdef get_default_format(self):
        print(f"ERROR, not subclassed {self.__class__}")

cdef class CharMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<char*>buf)[0] = <char>value
        return 0
    cdef get_itemsize(self): return sizeof(char)
    cdef get_default_format(self): return b"@b"

cdef class IntMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<i32*>buf)[0] = <i32>value
        return 0
    cdef get_itemsize(self): return sizeof(i32)
    cdef get_default_format(self): return b"@i"

cdef class UnsignedIntMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<u32*>buf)[0] = <u32>value
        return 0
    cdef get_itemsize(self): return sizeof(u32)
    cdef get_default_format(self): return b"@I"

cdef class ShortMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<short*>buf)[0] = <short>value
        return 0
    cdef get_itemsize(self): return sizeof(short)
    cdef get_default_format(self): return b"h" # Try without endian specifier

cdef class UnsignedShortMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<unsigned short*>buf)[0] = <unsigned short>value
        return 0
    cdef get_itemsize(self): return sizeof(unsigned short)
    cdef get_default_format(self): return b"@1H" # Try with repeat count

cdef class FloatMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<f32*>buf)[0] = <f32>(<f64>value)
        return 0
    cdef get_itemsize(self): return sizeof(f32)
    cdef get_default_format(self): return b"f"

cdef class DoubleMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        (<f64*>buf)[0] = <f64>value
        return 0
    cdef get_itemsize(self): return sizeof(f64)
    cdef get_default_format(self): return b"d"

cdef extern from *:
    void* addr_of_pyobject "(void*)"(object)

cdef class ObjectMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
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

    def __getbuffer__(ErrorBuffer self, Py_buffer* buffer, i32 flags):
        raise Exception(f"acquiring {self.label}")

    def __releasebuffer__(ErrorBuffer self, Py_buffer* buffer):
        raise Exception(f"releasing {self.label}")

#
# Structs
#
cdef struct MyStruct:
    signed char a
    signed char b
    i128 c
    i32 d
    i32 e

cdef struct SmallStruct:
    i32 a
    i32 b

cdef struct NestedStruct:
    SmallStruct x
    SmallStruct y
    i32 z

cdef packed struct PackedStruct:
    signed char a
    i32 b

cdef struct NestedPackedStruct:
    signed char a
    i32 b
    PackedStruct sub
    i32 c

cdef class MyStructMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        cdef MyStruct* s
        s = <MyStruct*>buf
        s.a, s.b, s.c, s.d, s.e = value
        return 0

    cdef get_itemsize(self): return sizeof(MyStruct)
    cdef get_default_format(self): return b"2cq2i"

cdef class NestedStructMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        cdef NestedStruct* s
        s = <NestedStruct*>buf
        s.x.a, s.x.b, s.y.a, s.y.b, s.z = value
        return 0

    cdef get_itemsize(self): return sizeof(NestedStruct)
    cdef get_default_format(self): return b"2T{ii}i"

cdef class PackedStructMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
        cdef PackedStruct* s
        s = <PackedStruct*>buf
        s.a, s.b = value
        return 0

    cdef get_itemsize(self): return sizeof(PackedStruct)
    cdef get_default_format(self): return b"^ci"

cdef class NestedPackedStructMockBuffer(MockBuffer):
    cdef i32 write(self, char* buf, object value) except -1:
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
    cdef i32 write(self, char* buf, object value) except -1:
        cdef LongComplex* s
        s = <LongComplex*>buf
        s.real, s.imag = value
        return 0

    cdef get_itemsize(self): return sizeof(LongComplex)
    cdef get_default_format(self): return b"Zg"


def print_offsets(*args, size, newline=true):
    sys.stdout.write(' '.join([str(item // size) for item in args]) + ('\n' if newline else ''))

def print_int_offsets(*args, newline=true):
    print_offsets(*args, size=sizeof(i32), newline=newline)

shape_5_3_4_list = [[list(range(k * 12 + j * 4, k * 12 + j * 4 + 4))
                        for j in range(3)]
                            for k in range(5)]

stride1 = 21 * 14
stride2 = 21
shape_9_14_21_list = [[list(range(k * stride1 + j * stride2, k * stride1 + j * stride2 + 21))
                           for j in range(14)]
                               for k in range(9)]
