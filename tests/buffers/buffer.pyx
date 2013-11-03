__doc__ = u"""
>>> b1 = TestBuffer()
>>> b2 = TestBufferRelease()
"""

import sys
if sys.version_info[0] >= 3:
    __doc__ += u"""
>>> ms = memoryview(s)
>>> ms.tobytes()
b'abcdefg'

>>> m1 = memoryview(b1)
__getbuffer__ called

Semantics changed in python 3.3
>> m1.tobytes()
__getbuffer__ called
b'abcdefg'

>>> m2 = memoryview(b2)
__getbuffer__ called

Semantics changed in python 3.3
>> m2.tobytes()
__getbuffer__ called
releasing!
b'abcdefg'

>>> del m1
>>> del m2
releasing!
"""

s = b"abcdefg"

cdef class TestBuffer:
    def __getbuffer__(self, Py_buffer* buffer, int flags):
        print u"__getbuffer__ called"
        buffer.buf = <char*>s
        buffer.obj = self
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
        print u"releasing!"

cdef class TestCompileWithDocstring(object):
    def __getbuffer__(self, Py_buffer* buffer, int flags):
        "I am a docstring!"
    def __releasebuffer__(self, Py_buffer* buf):
        "I am a docstring!"
