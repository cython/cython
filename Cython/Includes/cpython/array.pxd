"""
  array.pxd

  Cython interface to Python's array.array module.

  * 1D contiguous data view
  * tools for fast array creation, maximum C-speed and handiness
  * suitable as allround light weight auto-array within Cython code too

  Usage:

  >>> cimport array

  Usage through Cython buffer interface (Py2.3+):

    >>> def f(arg1, unsigned i, f64 dx)
    ...     array.array[f64] a = arg1
    ...     a[i] += dx

  Fast C-level new_array(_zeros), resize_array, copy_array, Py_SIZE(obj),
  zero_array

    cdef array.array[f64] k = array.copy(d)
    cdef array.array[f64] n = array.array(d, Py_SIZE(d) * 2 )
    cdef array.array[f64] m = array.zeros_like(FLOAT_TEMPLATE)
    array.resize(f, 200000)

  Zero overhead with naked data pointer views by union:
  _f, _d, _i, _c, _u, ...
  => Original C array speed + Python dynamic memory management

    cdef array.array a = inarray
    if
    a._d[2] += 0.66   # use as double array without extra casting

    f32 *subview = vector._f + 10  # starting from 10th element
    u16 *subview_buffer = vector._B + 4

  Suitable as lightweight arrays intra Cython without speed penalty.
  Replacement for C stack/malloc arrays; no trouble with refcounting,
  mem.leaks; seamless Python compatibility, buffer() optional


  last changes: 2009-05-15 rk
              : 2009-12-06 bp
              : 2012-05-02 andreasvc
              : (see revision control)
"""

extern from *:
    """
    #if CYTHON_COMPILING_IN_PYPY
    #ifdef _MSC_VER
    #pragma message ("This module uses CPython specific internals of 'array.array', which are not available in PyPy.")
    #else
    #warning This module uses CPython specific internals of 'array.array', which are not available in PyPy.
    #endif
    #endif
    """

from libc.string cimport memset, memcpy

from cpython.object cimport Py_SIZE
from cpython.ref cimport PyTypeObject, Py_TYPE
from cpython.exc cimport PyErr_BadArgument
from cpython.mem cimport PyObject_Malloc, PyObject_Free

extern from *:  # Hard-coded utility code hack.
    ctypedef class array.array [object arrayobject]
    ctypedef object GETF(array a, isize ix)
    ctypedef object SETF(array a, isize ix, object o)
    ctypedef struct arraydescr:  # [object arraydescr]:
        char typecode
        i32 itemsize
        GETF getitem    # PyObject * (*getitem)(struct arrayobject *, isize);
        SETF setitem    # i32 (*setitem)(struct arrayobject *, isize, PyObject *);

    ctypedef union __data_union:
        # views of ob_item:
        f32* as_floats       # direct float pointer access to buffer
        f64* as_doubles      # double ...
        i32* as_ints
        u32 *as_uints
        u16 *as_uchars
        signed char *as_schars
        char *as_chars
        u64 *as_ulongs
        i64 *as_longs
        u128 *as_ulonglongs
        i128 *as_longlongs
        i16 *as_shorts
        u16 *as_ushorts
        Py_UNICODE *as_pyunicodes
        void *as_voidptr

    ctypedef class array.array [object arrayobject]:
        cdef __cythonbufferdefaults__ = {'ndim' : 1, 'mode':'c'}

        cdef:
            isize ob_size
            arraydescr* ob_descr    # struct arraydescr *ob_descr;
            __data_union data

        def __getbuffer__(self, Py_buffer* info, i32 flags):
            # This implementation of getbuffer is geared towards Cython
            # requirements, and does not yet fulfill the PEP.
            # In particular strided access is always provided regardless
            # of flags
            item_count = Py_SIZE(self)

            info.suboffsets = NULL
            info.buf = self.data.as_chars
            info.readonly = 0
            info.ndim = 1
            info.itemsize = self.ob_descr.itemsize   # e.g. sizeof(float)
            info.len = info.itemsize * item_count

            info.shape = <isize*>PyObject_Malloc(sizeof(isize) + 2)
            if not info.shape:
                raise MemoryError()
            info.shape[0] = item_count      # constant regardless of resizing
            info.strides = &info.itemsize

            info.format = <char*>(info.shape + 1)
            info.format[0] = self.ob_descr.typecode
            info.format[1] = 0
            info.obj = self

        def __releasebuffer__(self, Py_buffer* info):
            PyObject_Free(info.shape)

    array newarrayobject(PyTypeObject* type, isize size, arraydescr *descr)

    # fast resize/realloc
    # not suitable for small increments; reallocation 'to the point'
    i32 resize(array self, isize n) except -1
    # efficient for small increments (not in Py2.3-)
    i32 resize_smart(array self, isize n) except -1

fn inline array clone(array template, isize length, bint zero):
    """ fast creation of a new array, given a template array.
    type will be same as template.
    if zero is true, new array will be initialized with zeroes."""
    cdef array op = newarrayobject(Py_TYPE(template), length, template.ob_descr)
    if zero and op is not None:
        memset(op.data.as_chars, 0, length * op.ob_descr.itemsize)
    return op

fn inline array copy(array self):
    """ make a copy of an array. """
    cdef array op = newarrayobject(Py_TYPE(self), Py_SIZE(self), self.ob_descr)
    memcpy(op.data.as_chars, self.data.as_chars, Py_SIZE(op) * op.ob_descr.itemsize)
    return op

fn inline i32 extend_buffer(array self, char* stuff, isize n) except -1:
    """ efficient appending of new stuff of same type
    (e.g. of same array type)
    n: number of elements (not number of bytes!) """
    cdef isize itemsize = self.ob_descr.itemsize
    cdef isize origsize = Py_SIZE(self)
    resize_smart(self, origsize + n)
    memcpy(self.data.as_chars + origsize * itemsize, stuff, n * itemsize)
    return 0

fn inline i32 extend(array self, array other) except -1:
    """ extend array with data from another array; types must match. """
    if self.ob_descr.typecode != other.ob_descr.typecode:
        PyErr_BadArgument()
    return extend_buffer(self, other.data.as_chars, Py_SIZE(other))

fn inline void zero(array self):
    """ set all elements of array to zero. """
    memset(self.data.as_chars, 0, Py_SIZE(self) * self.ob_descr.itemsize)
