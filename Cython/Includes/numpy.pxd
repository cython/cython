cdef extern from "Python.h":
    ctypedef int Py_intptr_t
    
cdef extern from "numpy/arrayobject.h":
    ctypedef Py_intptr_t npy_intp
    ctypedef struct PyArray_Descr:
        int elsize

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
            
            info.buf = <void*>self.data
            info.ndim = 2
            info.strides = <Py_ssize_t*>self.strides
            info.shape = <Py_ssize_t*>self.dimensions
            info.suboffsets = NULL
            info.format = "i"
            info.itemsize = self.descr.elsize
            info.readonly = not PyArray_ISWRITEABLE(self)

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
