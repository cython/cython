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
  
  Fast C-level new_array(_zeros), resize_array, copy_array, .length,
  zero_array
  
    cdef array.array[double] k = array.copy(d) 
    cdef array.array[double] n = array.array(d, d.length * 2 ) 
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
  mem.leaks; seamless Python compatibility, buffer() optionA
  

  IMPORTANT: arrayarray.h (arrayobject, arraydescr) is not part of 
             the official Python C-API so far; arrayarray.h is located 
             next to this file copy it to PythonXX/include or local or 
             somewhere on your -I path 

  last changes: 2009-05-15 rk
              : 2009-12-06 bp
"""
from libc cimport stdlib

cdef extern from "stdlib.h" nogil:
    void *memset(void *str, int c, size_t n)
    char *strcat(char *str1, char *str2)
    char *strncat(char *str1, char *str2, size_t n)
    void *memchr(void *str, int c, size_t n)
    int memcmp(void *str1, void *str2, size_t n)
    void *memcpy(void *str1, void *str2, size_t n)
    void *memmove(void *str1, void *str2, size_t n)


cdef extern from "arrayarray.h":
    ctypedef void PyTypeObject
    ctypedef short Py_UNICODE
    int PyErr_BadArgument()
    ctypedef class array.array [object arrayobject]
    ctypedef object GETF(array a, Py_ssize_t ix)
    ctypedef object SETF(array a, Py_ssize_t ix, object o)
    ctypedef struct arraydescr:  # [object arraydescr]:
            int typecode
            int itemsize
            GETF getitem    # PyObject * (*getitem)(struct arrayobject *, Py_ssize_t);
            SETF setitem    # int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *);

    ctypedef class array.array [object arrayobject]:
        cdef __cythonbufferdefaults__ = {'ndim' : 1, 'mode':'c'}
        
        cdef:
            PyTypeObject* ob_type
            
            int ob_size             # number of valid items; 
            unsigned length         # == ob_size (by union)
            
            char* ob_item           # to first item
            
            Py_ssize_t allocated    # bytes
            arraydescr* ob_descr    # struct arraydescr *ob_descr;
            object weakreflist      # /* List of weak references */

            # view's of ob_item:
            float* _f               # direct float pointer access to buffer
            double* _d              # double ...
            int*    _i
            unsigned *_I
            unsigned char *_B
            signed char *_b
            char *_c
            unsigned long *_L
            long *_l
            short *_h
            unsigned short *_H
            Py_UNICODE *_u
            void* _v

        def __getbuffer__(array self, Py_buffer* info, int flags):
            # This implementation of getbuffer is geared towards Cython
            # requirements, and does not yet fullfill the PEP.
            # In particular strided access is always provided regardless
            # of flags
            cdef unsigned rows, columns, itemsize
            
            info.suboffsets = NULL
            info.buf = self.ob_item
            info.readonly = 0
            info.ndim = 1
            info.itemsize = itemsize = self.ob_descr.itemsize   # e.g. sizeof(float)
            
            info.strides = <Py_ssize_t*> \
                           stdlib.malloc(sizeof(Py_ssize_t) * info.ndim * 2 + 2)
            info.shape = info.strides + 1
            info.shape[0] = self.ob_size            # number of items
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
        
    array newarrayobject(PyTypeObject* type, Py_ssize_t size,
                              arraydescr *descr)

    # fast resize/realloc
    # not suitable for small increments; reallocation 'to the point'
    int resize(array self, Py_ssize_t n)
    # efficient for small increments (not in Py2.3-)
    int resize_smart(array self, Py_ssize_t n)


#  fast creation of a new array - init with zeros 
#  yet you need a (any) template array of the same item type (but not same size)
cdef inline array zeros_like(array sametype):
    cdef array op = newarrayobject(<PyTypeObject*>sametype.ob_type, sametype.ob_size, sametype.ob_descr)
    if op:
        memset(op.ob_item, 0, op.ob_size * op.ob_descr.itemsize)
        return op

#  fast creation of a new array - no init with zeros
cdef inline array new_array(array sametype, unsigned n):
    return newarrayobject( <PyTypeObject*>sametype.ob_type, n, sametype.ob_descr)

#  fast creation of a new array - no init with zeros, same length 
cdef inline array empty_like(array sametype):
    return newarrayobject(<PyTypeObject*>sametype.ob_type, sametype.op.ob_size,
                           sametype.ob_descr)

cdef inline array copy(array self):
    cdef array op = newarrayobject(<PyTypeObject*>self.ob_type, self.ob_size,
                                   self.ob_descr)
    memcpy(op.ob_item, self.ob_item, op.ob_size * op.ob_descr.itemsize)
    return op

cdef inline int extend_buffer(array self, char* stuff, Py_ssize_t n):
    """ efficent appending of new stuff of same type (e.g. of same array type)
        n: number of elements (not number of bytes!)
    """
    cdef Py_ssize_t itemsize = self.ob_descr.itemsize, orgsize = self.ob_size
    if -1 == resize_smart(self, orgsize + n):
        return -1
    memcpy(self.ob_item + orgsize * itemsize, stuff, n * itemsize)

cdef inline int extend(array self, array other):
    if self.ob_descr.typecode != self.ob_descr.typecode:
        PyErr_BadArgument()
        return -1
    return extend_buffer(self, other.ob_item, other.ob_size)


cdef inline void zero(array op):
    memset(op.ob_item, 0, op.ob_size * op.ob_descr.itemsize)
