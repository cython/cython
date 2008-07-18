cdef extern from "Python.h":
    ctypedef struct PyObject



    ctypedef struct Py_buffer:
        void *buf
        Py_ssize_t len
        int readonly
        char *format
        int ndim
        Py_ssize_t *shape
        Py_ssize_t *strides
        Py_ssize_t *suboffsets
        Py_ssize_t itemsize
        void *internal

    
    int PyObject_GetBuffer(PyObject* obj, Py_buffer* view, int flags) except -1
    void PyObject_ReleaseBuffer(PyObject* obj, Py_buffer* view)

    void PyErr_Format(int, char*, ...)

    enum:
        PyExc_TypeError

#                  int PyObject_GetBuffer(PyObject *obj, Py_buffer *view,
#                       int flags)
