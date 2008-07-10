cdef extern from "Python.h":
    ctypedef int Py_intptr_t
    
cdef extern from "numpy/arrayobject.h":
    ctypedef class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef Py_intptr_t *dimensions
        cdef Py_intptr_t *strides
        cdef object base
        # descr not implemented yet here...
        cdef int flags
        cdef int itemsize
        cdef object weakreflist

    ctypedef unsigned int npy_uint8
    ctypedef unsigned int npy_uint16
    ctypedef unsigned int npy_uint32
    ctypedef unsigned int npy_uint64
    ctypedef unsigned int npy_uint96
    ctypedef unsigned int npy_uint128
    ctypedef signed int   npy_int64

    ctypedef float        npy_float32
    ctypedef float        npy_float64
    ctypedef float        npy_float80
    ctypedef float        npy_float96
    ctypedef float        npy_float128

ctypedef npy_int64 Tint64
