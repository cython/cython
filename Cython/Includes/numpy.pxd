cdef extern from "Python.h":
    ctypedef int Py_intptr_t
    
cdef extern from "numpy/arrayobject.h":
    ctypedef void PyArrayObject
    
    ctypedef class numpy.ndarray [object PyArrayObject]:
        cdef:
            char *data
            int nd
            Py_intptr_t *dimensions
            Py_intptr_t *strides
            object base
            # descr not implemented yet here...
            int flags
            int itemsize
            object weakreflist

        def __getbuffer__(self, Py_buffer* info, int flags):
       
            pass



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
