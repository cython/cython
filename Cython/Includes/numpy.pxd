cdef extern from "Python.h":
    ctypedef int Py_intptr_t
    
cdef extern from "numpy/arrayobject.h":
    ctypedef Py_intptr_t npy_intp
        
    cdef enum:
        NPY_BOOL,
        NPY_BYTE, NPY_UBYTE,
        NPY_SHORT, NPY_USHORT,
        NPY_INT, NPY_UINT,
        NPY_LONG, NPY_ULONG,
        NPY_LONGLONG, NPY_ULONGLONG,
        NPY_FLOAT, NPY_DOUBLE, NPY_LONGDOUBLE,
        NPY_CFLOAT, NPY_CDOUBLE, NPY_CLONGDOUBLE,
        NPY_OBJECT,
        NPY_STRING, NPY_UNICODE,
        NPY_VOID,
        NPY_NTYPES,
        NPY_NOTYPE,
        NPY_CHAR,  
        NPY_USERDEF

    ctypedef class numpy.ndarray [object PyArrayObject]:
        cdef __cythonbufferdefaults__ = {"mode": "strided"}
        
        cdef:
            char *data
            int ndim "nd"
            npy_intp *shape "dimensions" 
            npy_intp *strides

        # Note: This syntax (function definition in pxd files) is an
        # experimental exception made for __getbuffer__ and __releasebuffer__
        # -- the details of this may change.
        def __getbuffer__(ndarray self, Py_buffer* info, int flags):
            # This implementation of getbuffer is geared towards Cython
            # requirements, and does not yet fullfill the PEP (specifically,
            # Cython always requests and we always provide strided access,
            # so the flags are not even checked).
            
            if sizeof(npy_intp) != sizeof(Py_ssize_t):
                raise RuntimeError("Py_intptr_t and Py_ssize_t differs in size, numpy.pxd does not support this")

            info.buf = PyArray_DATA(self)
            info.ndim = PyArray_NDIM(self)
            info.strides = <Py_ssize_t*>PyArray_STRIDES(self)
            info.shape = <Py_ssize_t*>PyArray_DIMS(self)
            info.suboffsets = NULL
            info.itemsize = PyArray_ITEMSIZE(self)
            info.readonly = not PyArray_ISWRITEABLE(self)

            # Formats that are not tested and working in Cython are not
            # made available from this pxd file yet.
            cdef int t = PyArray_TYPE(self)
            cdef char* f = NULL  
            if   t == NPY_BYTE:       f = "b"
            elif t == NPY_UBYTE:      f = "B"
            elif t == NPY_SHORT:      f = "h"
            elif t == NPY_USHORT:     f = "H"
            elif t == NPY_INT:        f = "i"
            elif t == NPY_UINT:       f = "I"
            elif t == NPY_LONG:       f = "l"
            elif t == NPY_ULONG:      f = "L"
            elif t == NPY_LONGLONG:   f = "q"
            elif t == NPY_ULONGLONG:  f = "Q"
            elif t == NPY_FLOAT:      f = "f"
            elif t == NPY_DOUBLE:     f = "d"
            elif t == NPY_LONGDOUBLE: f = "g"
            elif t == NPY_OBJECT:     f = "O"

            if f == NULL:
                raise ValueError("only objects, int and float dtypes supported for ndarray buffer access so far (dtype is %d)" % t)
            info.format = f
            

    cdef void* PyArray_DATA(ndarray arr)
    cdef int PyArray_TYPE(ndarray arr)
    cdef int PyArray_NDIM(ndarray arr)
    cdef int PyArray_ISWRITEABLE(ndarray arr)
    cdef npy_intp PyArray_STRIDES(ndarray arr)
    cdef npy_intp PyArray_DIMS(ndarray arr)
    cdef Py_ssize_t PyArray_ITEMSIZE(ndarray arr)

    ctypedef signed int   npy_byte
    ctypedef signed int   npy_short
    ctypedef signed int   npy_int
    ctypedef signed int   npy_long
    ctypedef signed int   npy_longlong

    ctypedef unsigned int npy_ubyte
    ctypedef unsigned int npy_ushort
    ctypedef unsigned int npy_uint
    ctypedef unsigned int npy_ulong
    ctypedef unsigned int npy_ulonglong

    ctypedef float        npy_float
    ctypedef float        npy_double
    ctypedef float        npy_longdouble

    ctypedef signed int   npy_int8
    ctypedef signed int   npy_int16
    ctypedef signed int   npy_int32
    ctypedef signed int   npy_int64
    ctypedef signed int   npy_int96
    ctypedef signed int   npy_int128    

    ctypedef unsigned int npy_uint8
    ctypedef unsigned int npy_uint16
    ctypedef unsigned int npy_uint32
    ctypedef unsigned int npy_uint64
    ctypedef unsigned int npy_uint96
    ctypedef unsigned int npy_uint128

    ctypedef float        npy_float32
    ctypedef float        npy_float64
    ctypedef float        npy_float80
    ctypedef float        npy_float96
    ctypedef float        npy_float128

# Typedefs that matches the runtime dtype objects in
# the numpy module.

# The ones that are commented out needs an IFDEF function
# in Cython to enable them only on the right systems.

ctypedef npy_int8       int8_t
ctypedef npy_int16      int16_t
ctypedef npy_int32      int32_t
ctypedef npy_int64      int64_t
#ctypedef npy_int96      int96_t
#ctypedef npy_int128     int128_t

ctypedef npy_uint8      uint8_t
ctypedef npy_uint16     uint16_t
ctypedef npy_uint32     uint32_t
ctypedef npy_uint64     uint64_t
#ctypedef npy_uint96     uint96_t
#ctypedef npy_uint128    uint128_t

ctypedef npy_float32    float32_t
ctypedef npy_float64    float64_t
#ctypedef npy_float80    float80_t
#ctypedef npy_float128   float128_t

# The int types are mapped a bit surprising --
# numpy.int corresponds to 'l' and numpy.long to 'q'
ctypedef npy_long       int_t
ctypedef npy_longlong   long_t

ctypedef npy_ulong      uint_t
ctypedef npy_ulonglong  ulong_t

ctypedef npy_double      float_t
ctypedef npy_double     double_t
ctypedef npy_longdouble longdouble_t

