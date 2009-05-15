# NumPy static imports for Cython
#
# This also defines backwards-compatability buffer acquisition
# code for use in Python 2.x (or Python <= 2.5 when NumPy starts
# implementing PEP-3118 directly).


# Because of laziness, the format string of the buffer is statically
# allocated. Increase the size if this is not enough, or submit a
# patch to do this properly.

DEF _buffer_format_string_len = 255

cimport python_buffer as pybuf
cimport stdlib

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
        NPY_USERDEF,

        NPY_C_CONTIGUOUS,
        NPY_F_CONTIGUOUS
        
    ctypedef class numpy.dtype [object PyArray_Descr]:
        cdef int type_num
        cdef int itemsize "elsize"
        cdef char byteorder
        cdef object fields
        cdef object names


    ctypedef class numpy.ndarray [object PyArrayObject]:
        cdef __cythonbufferdefaults__ = {"mode": "strided"}
        
        cdef:
            char *data
            int ndim "nd"
            npy_intp *shape "dimensions" 
            npy_intp *strides
            int flags
            dtype descr

        # Note: This syntax (function definition in pxd files) is an
        # experimental exception made for __getbuffer__ and __releasebuffer__
        # -- the details of this may change.
        def __getbuffer__(ndarray self, Py_buffer* info, int flags):
            # This implementation of getbuffer is geared towards Cython
            # requirements, and does not yet fullfill the PEP.
            # In particular strided access is always provided regardless
            # of flags
            cdef int copy_shape, i, ndim
            cdef int endian_detector = 1
            cdef bint little_endian = ((<char*>&endian_detector)[0] != 0)
            
            ndim = PyArray_NDIM(self)
            
            if sizeof(npy_intp) != sizeof(Py_ssize_t):
                copy_shape = 1
            else:
                copy_shape = 0

            if ((flags & pybuf.PyBUF_C_CONTIGUOUS == pybuf.PyBUF_C_CONTIGUOUS)
                and not PyArray_CHKFLAGS(self, NPY_C_CONTIGUOUS)):
                raise ValueError("ndarray is not C contiguous")
                
            if ((flags & pybuf.PyBUF_F_CONTIGUOUS == pybuf.PyBUF_F_CONTIGUOUS)
                and not PyArray_CHKFLAGS(self, NPY_F_CONTIGUOUS)):
                raise ValueError("ndarray is not Fortran contiguous")

            info.buf = PyArray_DATA(self)
            info.ndim = ndim
            if copy_shape:
                # Allocate new buffer for strides and shape info. This is allocated
                # as one block, strides first.
                info.strides = <Py_ssize_t*>stdlib.malloc(sizeof(Py_ssize_t) * ndim * 2)
                info.shape = info.strides + ndim
                for i in range(ndim):
                    info.strides[i] = PyArray_STRIDES(self)[i]
                    info.shape[i] = PyArray_DIMS(self)[i]
            else:
                info.strides = <Py_ssize_t*>PyArray_STRIDES(self)
                info.shape = <Py_ssize_t*>PyArray_DIMS(self)
            info.suboffsets = NULL
            info.itemsize = PyArray_ITEMSIZE(self)
            info.readonly = not PyArray_ISWRITEABLE(self)

            cdef int t
            cdef char* f = NULL
            cdef dtype descr = self.descr
            cdef list stack
            cdef int offset

            cdef bint hasfields = PyDataType_HASFIELDS(descr)

            if not hasfields and not copy_shape:
                # do not call releasebuffer
                info.obj = None
            else:
                # need to call releasebuffer
                info.obj = self

            if not hasfields:
                t = descr.type_num
                if ((descr.byteorder == '>' and little_endian) or
                    (descr.byteorder == '<' and not little_endian)):
                    raise ValueError("Non-native byte order not supported")
                if   t == NPY_BYTE:        f = "b"
                elif t == NPY_UBYTE:       f = "B"
                elif t == NPY_SHORT:       f = "h"
                elif t == NPY_USHORT:      f = "H"
                elif t == NPY_INT:         f = "i"
                elif t == NPY_UINT:        f = "I"
                elif t == NPY_LONG:        f = "l"
                elif t == NPY_ULONG:       f = "L"
                elif t == NPY_LONGLONG:    f = "q"
                elif t == NPY_ULONGLONG:   f = "Q"
                elif t == NPY_FLOAT:       f = "f"
                elif t == NPY_DOUBLE:      f = "d"
                elif t == NPY_LONGDOUBLE:  f = "g"
                elif t == NPY_CFLOAT:      f = "Zf"
                elif t == NPY_CDOUBLE:     f = "Zd"
                elif t == NPY_CLONGDOUBLE: f = "Zg"
                elif t == NPY_OBJECT:      f = "O"
                else:
                    raise ValueError("unknown dtype code in numpy.pxd (%d)" % t)
                info.format = f
                return
            else:
                info.format = <char*>stdlib.malloc(_buffer_format_string_len)
                info.format[0] = '^' # Native data types, manual alignment
                offset = 0
                f = _util_dtypestring(descr, info.format + 1,
                                      info.format + _buffer_format_string_len,
                                      &offset)
                f[0] = 0 # Terminate format string

        def __releasebuffer__(ndarray self, Py_buffer* info):
            if PyArray_HASFIELDS(self):
                stdlib.free(info.format)
            if sizeof(npy_intp) != sizeof(Py_ssize_t):
                stdlib.free(info.strides)
                # info.shape was stored after info.strides in the same block
            

    cdef void* PyArray_DATA(ndarray arr)
    cdef int PyArray_TYPE(ndarray arr)
    cdef int PyArray_NDIM(ndarray arr)
    cdef int PyArray_ISWRITEABLE(ndarray arr)
    cdef npy_intp* PyArray_STRIDES(ndarray arr)
    cdef npy_intp* PyArray_DIMS(ndarray arr)
    cdef int PyArray_ITEMSIZE(ndarray arr)
    cdef int PyArray_CHKFLAGS(ndarray arr, int flags)
    cdef int PyArray_HASFIELDS(ndarray arr)

    cdef int PyDataType_HASFIELDS(dtype obj)

    ctypedef signed char      npy_byte
    ctypedef signed short     npy_short
    ctypedef signed int       npy_int
    ctypedef signed long      npy_long
    ctypedef signed long long npy_longlong

    ctypedef unsigned char      npy_ubyte
    ctypedef unsigned short     npy_ushort
    ctypedef unsigned int       npy_uint
    ctypedef unsigned long      npy_ulong
    ctypedef unsigned long long npy_ulonglong

    ctypedef float        npy_float
    ctypedef double       npy_double
    ctypedef long double  npy_longdouble

    ctypedef signed char        npy_int8
    ctypedef signed short       npy_int16
    ctypedef signed int         npy_int32
    ctypedef signed long long   npy_int64
    ctypedef signed long long   npy_int96
    ctypedef signed long long   npy_int128    

    ctypedef unsigned char      npy_uint8
    ctypedef unsigned short     npy_uint16
    ctypedef unsigned int       npy_uint32
    ctypedef unsigned long long npy_uint64
    ctypedef unsigned long long npy_uint96
    ctypedef unsigned long long npy_uint128

    ctypedef float        npy_float32
    ctypedef double       npy_float64
    ctypedef long double  npy_float80
    ctypedef long double  npy_float96
    ctypedef long double  npy_float128

    ctypedef float complex        npy_complex64
    ctypedef double complex       npy_complex128
    ctypedef long double complex  npy_complex120
    ctypedef long double complex  npy_complex192
    ctypedef long double complex  npy_complex256

    ctypedef struct npy_cfloat:
        float real
        float imag

    ctypedef struct npy_cdouble:
        float real
        float imag

    ctypedef struct npy_clongdouble:
        float real
        float imag

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

ctypedef npy_complex64    complex64_t
ctypedef npy_complex128   complex128_t

# The int types are mapped a bit surprising --
# numpy.int corresponds to 'l' and numpy.long to 'q'
ctypedef npy_long       int_t
ctypedef npy_longlong   long_t


ctypedef npy_ulong      uint_t
ctypedef npy_ulonglong  ulong_t

ctypedef npy_double     float_t
ctypedef npy_double     double_t
ctypedef npy_longdouble longdouble_t

ctypedef npy_cfloat      cfloat_t
ctypedef npy_cdouble     cdouble_t
ctypedef npy_clongdouble clongdouble_t

ctypedef npy_cdouble     complex_t

cdef inline char* _util_dtypestring(dtype descr, char* f, char* end, int* offset) except NULL:
    # Recursive utility function used in __getbuffer__ to get format
    # string. The new location in the format string is returned.

    cdef dtype child
    cdef int delta_offset
    cdef tuple i
    cdef int endian_detector = 1
    cdef bint little_endian = ((<char*>&endian_detector)[0] != 0)
    
    for i in descr.fields.itervalues():
        child = i[0]
        new_offset = i[1]

        if (end - f) - (new_offset - offset[0]) < 15:
            raise RuntimeError("Format string allocated too short, see comment in numpy.pxd")

        if ((child.byteorder == '>' and little_endian) or
            (child.byteorder == '<' and not little_endian)):
            raise ValueError("Non-native byte order not supported")
            # One could encode it in the format string and have Cython
            # complain instead, BUT: < and > in format strings also imply
            # standardized sizes for datatypes, and we rely on native in
            # order to avoid reencoding data types based on their size.
            #
            # A proper PEP 3118 exporter for other clients than Cython
            # must deal properly with this!
        
        # Output padding bytes
        while offset[0] < new_offset:
            f[0] = 120 # "x"; pad byte
            f += 1
            offset[0] += 1

        offset[0] += child.itemsize
            
        if not PyDataType_HASFIELDS(child):
            t = child.type_num
            if end - f < 5:
                raise RuntimeError("Format string allocated too short.")

            # Until ticket #99 is fixed, use integers to avoid warnings
            if   t == NPY_BYTE:        f[0] =  98 #"b"
            elif t == NPY_UBYTE:       f[0] =  66 #"B"
            elif t == NPY_SHORT:       f[0] = 104 #"h"
            elif t == NPY_USHORT:      f[0] =  72 #"H"
            elif t == NPY_INT:         f[0] = 105 #"i"
            elif t == NPY_UINT:        f[0] =  73 #"I"
            elif t == NPY_LONG:        f[0] = 108 #"l"
            elif t == NPY_ULONG:       f[0] = 76  #"L"
            elif t == NPY_LONGLONG:    f[0] = 113 #"q"
            elif t == NPY_ULONGLONG:   f[0] = 81  #"Q"
            elif t == NPY_FLOAT:       f[0] = 102 #"f"
            elif t == NPY_DOUBLE:      f[0] = 100 #"d"
            elif t == NPY_LONGDOUBLE:  f[0] = 103 #"g"
            elif t == NPY_CFLOAT:      f[0] = 90; f[1] = 102; f += 1 # Zf
            elif t == NPY_CDOUBLE:     f[0] = 90; f[1] = 100; f += 1 # Zd
            elif t == NPY_CLONGDOUBLE: f[0] = 90; f[1] = 103; f += 1 # Zg
            elif t == NPY_OBJECT:      f[0] = 79 #"O"
            else:
                raise ValueError("unknown dtype code in numpy.pxd (%d)" % t)
            f += 1
        else:
            # Cython ignores struct boundary information ("T{...}"),
            # so don't output it
            f = _util_dtypestring(child, f, end, offset)
    return f
                
