__doc__ = u"""
>>> b1 = TestBuffer()
>>> b2 = TestBufferRelease()
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ += u"""
>>> ms = memoryview(s)
>>> ms.tobytes()
bytearray(b'abcdefg')

>>> m1 = memoryview(b1)
>>> m1.tobytes()
locking!
bytearray(b'abcdefg')

>>> m2 = memoryview(b2)
>>> m2.tobytes()
locking!
unlocking!
bytearray(b'abcdefg')

>>> del m1
>>> del m2
releasing!
"""

s = "abcdefg"

cdef class TestBuffer:
    def __getbuffer__(self, Py_buffer* buffer, int flags):
        if buffer is NULL:
            print u"locking!"
            return
        buffer.buf = <char*>s
        buffer.len = len(s)
        buffer.readonly = 0
        buffer.format = "B"
        buffer.ndim = 0
        buffer.shape = NULL
        buffer.strides = NULL
        buffer.suboffsets = NULL
        buffer.itemsize = 1
        buffer.internal = NULL

cdef class TestBufferRelease(TestBuffer):
    def __releasebuffer__(self, Py_buffer* buffer):
        if buffer is NULL:
            print u"unlocking!"
        else:
            print u"releasing!"
