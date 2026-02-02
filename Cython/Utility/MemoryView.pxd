# from cpython cimport ...

cimport cython
cdef extern from "Python.h":
    ctypedef struct PyObject
    ctypedef void *PyThread_type_lock

cdef extern from *:
    ctypedef struct {{memviewslice_name}}:
        pass

    ctypedef struct __pyx_buffer "Py_buffer":
        PyObject *obj

    ctypedef struct __Pyx_TypeInfo:
        pass

    cdef struct __pyx_memoryview "__pyx_memoryview_obj":
        Py_buffer view
        PyObject *obj
        const __Pyx_TypeInfo *typeinfo

    ctypedef int __pyx_atomic_int_type


@cname("__pyx_array")
cdef class array:

    cdef:
        char *data
        Py_ssize_t len
        char *format
        int ndim
        Py_ssize_t *_shape
        Py_ssize_t *_strides
        Py_ssize_t itemsize
        unicode mode  # FIXME: this should have been a simple 'char'
        bytes _format
        void (*callback_free_data)(void *data) noexcept
        # cdef object _memview
        cdef bint free_data
        cdef bint dtype_is_object

    @cname('get_memview')
    cdef get_memview(self)

@cname("__pyx_array_new")
cdef array array_cwrapper(tuple shape, Py_ssize_t itemsize, char *format, const char *c_mode, char *buf)

@cname('__pyx_MemviewEnum')
cdef class Enum(object):
    pass

cdef Enum generic
cdef Enum strided
cdef Enum indirect
# Disable generic_contiguous, as it is a troublemaker
#cdef generic_contiguous = Enum("<contiguous and direct or indirect>")
cdef Enum contiguous
cdef Enum indirect_contiguous

@cname('__pyx_memoryview')
cdef class memoryview:

    cdef object obj
    cdef object _size
    # This comes before acquisition_count so can't be removed without breaking ABI compatibility
    cdef void* _unused
    cdef PyThread_type_lock lock
    cdef __pyx_atomic_int_type acquisition_count
    cdef Py_buffer view
    cdef int flags
    cdef bint dtype_is_object
    cdef const __Pyx_TypeInfo *typeinfo

    cdef char *get_item_pointer(memoryview self, object index) except NULL
    cdef is_slice(self, obj)
    cdef setitem_slice_assignment(self, dst, src)
    cdef setitem_slice_assign_scalar(self, memoryview dst, value)
    cdef setitem_indexed(self, index, value)
    cdef convert_item_to_object(self, char *itemp)
    cdef assign_item_from_object(self, char *itemp, object value)
    cdef _get_base(self)

@cname('__pyx_memoryview_new')
cdef memoryview_cwrapper(object o, int flags, bint dtype_is_object, const __Pyx_TypeInfo *typeinfo)

@cname('__pyx_memoryview_check')
cdef inline bint memoryview_check(object o) noexcept:
    return isinstance(o, memoryview)

@cname('__pyx_memoryview_slice_memviewslice')
cdef int slice_memviewslice(
        {{memviewslice_name}} *dst,
        Py_ssize_t shape, Py_ssize_t stride, Py_ssize_t suboffset,
        int dim, int new_ndim, int *suboffset_dim,
        Py_ssize_t start, Py_ssize_t stop, Py_ssize_t step,
        int have_start, int have_stop, int have_step,
        bint is_slice) except -1 nogil

@cname('__pyx_memslice_transpose')
cdef int transpose_memslice({{memviewslice_name}} *memslice) except -1 nogil

@cname('__pyx_memoryview_fromslice')
cdef memoryview_fromslice({{memviewslice_name}} memviewslice,
                          int ndim,
                          object (*to_object_func)(char *),
                          int (*to_dtype_func)(char *, object) except 0,
                          bint dtype_is_object)

@cname('__pyx_memoryview_copy_contents')
cdef int memoryview_copy_contents({{memviewslice_name}} src,
                                  {{memviewslice_name}} dst,
                                  int src_ndim, int dst_ndim,
                                  bint dtype_is_object) except -1 nogil
