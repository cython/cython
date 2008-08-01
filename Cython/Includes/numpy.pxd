cdef extern from "Python.h":
    ctypedef int Py_intptr_t
    
cdef extern from "numpy/arrayobject.h":
    ctypedef void PyArrayObject
    int PyArray_TYPE(PyObject* arr)
    
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
            cdef int typenum = PyArray_TYPE(self)

            
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
