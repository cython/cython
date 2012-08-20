"""
  array.pxd
  
  Cython interface to Python's array.array module.
  
  * 1D contiguous data view
  * tools for fast array creation, maximum C-speed and handiness
  * suitable as allround light weight auto-array within Cython code too
  
  Usage:
  
  >>> cimport array

  Usage through Cython buffer interface (Py2.3+):  
  
    >>> def f(arg1, unsigned i, double dx)
    ...     array.array[double] a = arg1
    ...     a[i] += dx
  
  Fast C-level new_array(_zeros), resize_array, copy_array, Py_SIZE(obj),
  zero_array
  
    cdef array.array[double] k = array.copy(d) 
    cdef array.array[double] n = array.array(d, Py_SIZE(d) * 2 )
    cdef array.array[double] m = array.zeros_like(FLOAT_TEMPLATE)
    array.resize(f, 200000)
  
  Zero overhead with naked data pointer views by union: 
  _f, _d, _i, _c, _u, ... 
  => Original C array speed + Python dynamic memory management

    cdef array.array a = inarray
    if 
    a._d[2] += 0.66   # use as double array without extra casting
  
    float *subview = vector._f + 10  # starting from 10th element
    unsigned char *subview_buffer = vector._B + 4  
    
  Suitable as lightweight arrays intra Cython without speed penalty. 
  Replacement for C stack/malloc arrays; no trouble with refcounting, 
  mem.leaks; seamless Python compatibility, buffer() optional
  

  last changes: 2009-05-15 rk
              : 2009-12-06 bp
              : 2012-05-02 andreasvc
              : (see revision control)
"""
from libc cimport stdlib
from libc.string cimport strcat, strncat, \
    memset, memchr, memcmp, memcpy, memmove

from cpython.object cimport Py_SIZE
from cpython.ref cimport PyTypeObject, Py_TYPE
from cpython.exc cimport PyErr_BadArgument

cdef extern from *:  # Hard-coded utility code hack.
    ctypedef class array.array [object arrayobject]
    ctypedef object GETF(array a, Py_ssize_t ix)
    ctypedef object SETF(array a, Py_ssize_t ix, object o)
    ctypedef struct arraydescr:  # [object arraydescr]:
            int typecode
            int itemsize
            GETF getitem    # PyObject * (*getitem)(struct arrayobject *, Py_ssize_t);
            SETF setitem    # int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *);

    ctypedef union __data_union:
        # views of ob_item:
        float* as_floats        # direct float pointer access to buffer
        double* as_doubles      # double ...
        int*    as_ints
        unsigned int *as_uints
        unsigned char *as_uchars
        signed char *as_schars
        char *as_chars
        unsigned long *as_ulongs
        long *as_longs
        short *as_shorts
        unsigned short *as_ushorts
        Py_UNICODE *as_pyunicodes
        void *as_voidptr

    ctypedef class array.array [object arrayobject]:
        cdef __cythonbufferdefaults__ = {'ndim' : 1, 'mode':'c'}
        
        cdef:
            Py_ssize_t ob_size
            arraydescr* ob_descr    # struct arraydescr *ob_descr;
            __data_union data

        def __getbuffer__(array self, Py_buffer* info, int flags):
            # This implementation of getbuffer is geared towards Cython
            # requirements, and does not yet fullfill the PEP.
            # In particular strided access is always provided regardless
            # of flags
            cdef unsigned rows, columns, itemsize
            
            info.suboffsets = NULL
            info.buf = self.data.as_chars
            info.readonly = 0
            info.ndim = 1
            info.itemsize = itemsize = self.ob_descr.itemsize   # e.g. sizeof(float)
            
            info.strides = <Py_ssize_t*> \
                           stdlib.malloc(sizeof(Py_ssize_t) * info.ndim * 2 + 2)
            info.shape = info.strides + 1
            info.shape[0] = Py_SIZE(self)            # number of items
            info.strides[0] = info.itemsize

            info.format = <char*>(info.strides + 2 * info.ndim)
            info.format[0] = self.ob_descr.typecode
            info.format[1] = 0
            info.obj = self

        def __releasebuffer__(array self, Py_buffer* info):
            #if PyArray_HASFIELDS(self):
            #    stdlib.free(info.format)
            #if sizeof(npy_intp) != sizeof(Py_ssize_t):
            stdlib.free(info.strides)
        
    array newarrayobject(PyTypeObject* type, Py_ssize_t size, arraydescr *descr)

    # fast resize/realloc
    # not suitable for small increments; reallocation 'to the point'
    int resize(array self, Py_ssize_t n)
    # efficient for small increments (not in Py2.3-)
    int resize_smart(array self, Py_ssize_t n)


cdef inline array clone(array template, Py_ssize_t length, bint zero):
    """ fast creation of a new array, given a template array.
    type will be same as template.
    if zero is true, new array will be initialized with zeroes."""
    cdef array op
    op = newarrayobject(Py_TYPE(template), length, template.ob_descr)
    if zero and op is not None:
        memset(op.data.as_chars, 0, length * op.ob_descr.itemsize)
    return op

cdef inline array copy(array self):
    """ make a copy of an array. """
    cdef array op
    op = newarrayobject(Py_TYPE(self), Py_SIZE(self), self.ob_descr)
    memcpy(op.data.as_chars, self.data.as_chars, Py_SIZE(op) * op.ob_descr.itemsize)
    return op

cdef inline int extend_buffer(array self, char* stuff, Py_ssize_t n):
    """ efficent appending of new stuff of same type
    (e.g. of same array type)
    n: number of elements (not number of bytes!) """
    cdef Py_ssize_t itemsize = self.ob_descr.itemsize
    cdef Py_ssize_t orgsize = Py_SIZE(self)
    if resize_smart(self, orgsize + n) == -1:
        return -1
    memcpy(self.data.as_chars + orgsize * itemsize, stuff, n * itemsize)

cdef inline int extend(array self, array other):
    """ extend array with data from another array; types must match. """
    if self.ob_descr.typecode != self.ob_descr.typecode:
        PyErr_BadArgument()
        return -1
    return extend_buffer(self, other.data.as_chars, Py_SIZE(other))

cdef inline void zero(array op):
    """ set all elements of array to zero. """
    memset(op.data.as_chars, 0, Py_SIZE(op) * op.ob_descr.itemsize)
