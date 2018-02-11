import sys

__doc__ = u""

if sys.version_info[:2] == (2, 6):
    __doc__ += u"""
>>> memoryview = _memoryview
"""

__doc__ += u"""
>>> b1 = UserBuffer1()
>>> m1 = memoryview(b1)
>>> m1.tolist()
[0, 1, 2, 3, 4]
>>> del m1, b1
"""

__doc__ += u"""
>>> b2 = UserBuffer2()
>>> m2 = memoryview(b2)
UserBuffer2: getbuffer
>>> m2.tolist()
[5, 6, 7, 8, 9]
>>> del m2, b2
UserBuffer2: release
"""

cdef extern from *:
    ctypedef struct Py_buffer # redeclared
    enum: PyBUF_SIMPLE
    int PyBuffer_FillInfo(Py_buffer *, object, void *, Py_ssize_t, bint, int) except -1
    int  PyObject_GetBuffer(object, Py_buffer *, int) except -1
    void PyBuffer_Release(Py_buffer *)

cdef char global_buf[5]
global_buf[0:5] = [0, 1, 2, 3, 4]

cdef class UserBuffer1:

    def __getbuffer__(self, Py_buffer* view, int flags):
        PyBuffer_FillInfo(view, None, global_buf, 5, 1, flags)

cdef class UserBuffer2:
    cdef char buf[5]

    def __cinit__(self):
        self.buf[0:5] = [5, 6, 7, 8, 9]

    def __getbuffer__(self, Py_buffer* view, int flags):
        print('UserBuffer2: getbuffer')
        PyBuffer_FillInfo(view, self, self.buf, 5, 0, flags)

    def __releasebuffer__(self, Py_buffer* view):
        print('UserBuffer2: release')


cdef extern from *:
    ctypedef struct PyBuffer"Py_buffer":
        void *buf
        Py_ssize_t len
        bint readonly

cdef class _memoryview:

    """
    Memory
    """

    cdef PyBuffer view

    def __cinit__(self, obj):
        cdef Py_buffer *view = <Py_buffer*>&self.view
        PyObject_GetBuffer(obj, view, PyBUF_SIMPLE)

    def __dealloc__(self):
        cdef Py_buffer *view = <Py_buffer*>&self.view
        PyBuffer_Release(view )
        
    def __getbuffer__(self, Py_buffer *view, int flags):
        PyBuffer_FillInfo(view, self,
                          self.view.buf, self.view.len,
                          self.view.readonly, flags)
    def tolist(self):
        cdef char *b = <char *> self.view.buf
        return [b[i] for i in range(self.view.len)]
