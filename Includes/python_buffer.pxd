# Please see the Python header files (object.h) for docs

cdef extern from "Python.h":
    ctypedef void PyObject
    
    ctypedef struct bufferinfo:
        void *buf     
        Py_ssize_t len
        Py_ssize_t itemsize            
        int readonly
        int ndim
        char *format
        Py_ssize_t *shape
        Py_ssize_t *strides
        Py_ssize_t *suboffsets
        void *internal
    ctypedef bufferinfo Py_buffer

    cdef enum:
        PyBUF_SIMPLE,
        PyBUF_WRITABLE,
        PyBUF_WRITEABLE, # backwards compatability
        PyBUF_FORMAT,
        PyBUF_ND,
        PyBUF_STRIDES,
        PyBUF_C_CONTIGUOUS,
        PyBUF_F_CONTIGUOUS,
        PyBUF_ANY_CONTIGUOUS,
        PyBUF_INDIRECT,
        PyBUF_CONTIG,
        PyBUF_CONTIG_RO,
        PyBUF_STRIDED,
        PyBUF_STRIDED_RO,
        PyBUF_RECORDS,
        PyBUF_RECORDS_RO,
        PyBUF_FULL,
        PyBUF_FULL_RO,
        PyBUF_READ,
        PyBUF_WRITE,
        PyBUF_SHADOW

    int PyObject_CheckBuffer(PyObject* obj)
    int PyObject_GetBuffer(PyObject *obj, Py_buffer *view, int flags)
    void PyObject_ReleaseBuffer(PyObject *obj, Py_buffer *view)
    void* PyBuffer_GetPointer(Py_buffer *view, Py_ssize_t *indices)
    int PyBuffer_SizeFromFormat(char *) # actually const char
    int PyBuffer_ToContiguous(void *buf, Py_buffer *view, Py_ssize_t len, char fort)
    int PyBuffer_FromContiguous(Py_buffer *view, void *buf, Py_ssize_t len, char fort)
    int PyObject_CopyData(PyObject *dest, PyObject *src)
    int PyBuffer_IsContiguous(Py_buffer *view, char fort)
    void PyBuffer_FillContiguousStrides(int ndims, 
                                        Py_ssize_t *shape, 
                                        Py_ssize_t *strides,
                                        int itemsize,
                                        char fort)
    int PyBuffer_FillInfo(Py_buffer *view, void *buf,
                          Py_ssize_t len, int readonly,
                          int flags)

    PyObject* PyObject_Format(PyObject* obj,
                              PyObject *format_spec)
