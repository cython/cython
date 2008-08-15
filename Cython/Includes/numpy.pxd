from stdlib cimport malloc, free


cdef extern from "Python.h":
    ctypedef int Py_intptr_t
    
cdef extern from "numpy/arrayobject.h":
    ctypedef Py_intptr_t npy_intp
    ctypedef struct PyArray_Descr:
        int elsize
        char byteorder
        
        
    ctypedef class numpy.ndarray [object PyArrayObject]

    int PyArray_NDIM(ndarray)
    bint PyTypeNum_ISNUMBER(int)
    bint PyTypeNum_ISCOMPLEX(int)


    ctypedef class numpy.ndarray [object PyArrayObject]:
        cdef:
            char *data
            int nd
            npy_intp *dimensions 
            npy_intp *strides
            object base
            # descr not implemented yet here...
            int flags
            int itemsize
            object weakreflist
            PyArray_Descr* descr

        def __getbuffer__(ndarray self, Py_buffer* info, int flags):
            if sizeof(npy_intp) != sizeof(Py_ssize_t):
                raise RuntimeError("Py_intptr_t and Py_ssize_t differs in size, numpy.pxd does not support this")

            cdef int typenum = PyArray_TYPE(self)
            # NumPy format codes doesn't completely match buffer codes;
            # seems safest to retranslate.
            cdef char* base_codes = "?bBhHiIlLqQfdgfdgO"
            if not base_codes[typenum] == 'O' and not PyTypeNum_ISNUMBER(typenum):
                raise ValueError, "Only numeric and object NumPy types currently supported."
            
            info.buf = <void*>self.data
            info.ndim = PyArray_NDIM(self)
            info.strides = <Py_ssize_t*>self.strides
            info.shape = <Py_ssize_t*>self.dimensions
            info.suboffsets = NULL
            info.itemsize = self.descr.elsize
            info.readonly = not PyArray_ISWRITEABLE(self)
            
            cdef char* fp
            fp = info.format = <char*>malloc(4)
            fp[0] = self.descr.byteorder
            cdef bint is_complex = not not PyTypeNum_ISCOMPLEX(typenum)
            if is_complex:
                fp[1] = 'Z'
            fp[1+is_complex] = base_codes[typenum]
            fp[2+is_complex] = 0
            

        def __releasebuffer__(ndarray self, Py_buffer* info):
            free(info.format)


            # PS TODO TODO!: Py_ssize_t vs Py_intptr_t

            
##   PyArrayObject *arr = (PyArrayObject*)obj;
##   PyArray_Descr *type = (PyArray_Descr*)arr->descr;

  
##   int typenum = PyArray_TYPE(obj);
##   if (!PyTypeNum_ISNUMBER(typenum)) {
##     PyErr_Format(PyExc_TypeError, "Only numeric NumPy types currently supported.");
##     return -1;
##   }

##   /*
##   NumPy format codes doesn't completely match buffer codes;
##   seems safest to retranslate.
##                             01234567890123456789012345*/
##   const char* base_codes = "?bBhHiIlLqQfdgfdgO";

##   char* format = (char*)malloc(4);
##   char* fp = format;
##   *fp++ = type->byteorder;
##   if (PyTypeNum_ISCOMPLEX(typenum)) *fp++ = 'Z';
##   *fp++ = base_codes[typenum];
##   *fp = 0;

##   view->buf = arr->data;
##   view->readonly = !PyArray_ISWRITEABLE(obj);
##   view->ndim = PyArray_NDIM(arr);
##   view->strides = PyArray_STRIDES(arr);
##   view->shape = PyArray_DIMS(arr);
##   view->suboffsets = NULL;
##   view->format = format;
##   view->itemsize = type->elsize;

##   view->internal = 0;
##   return 0;
##             print "hello" + str(43) + "asdf" + "three"
##             pass

    cdef int PyArray_TYPE(ndarray arr)
    cdef int PyArray_ISWRITEABLE(ndarray arr)

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


ctypedef npy_int64 int64
