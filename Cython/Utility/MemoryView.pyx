########## CythonArray ##########

cdef extern from "stdlib.h":
    void *malloc(size_t)
    void free(void *)

cdef extern from "Python.h":

    cdef enum:
        PyBUF_C_CONTIGUOUS,
        PyBUF_F_CONTIGUOUS,
        PyBUF_ANY_CONTIGUOUS
        PyBUF_FORMAT

cdef extern from *:
    object __pyx_memoryview_new(object obj, int flags)

@cname("__pyx_array")
cdef class array:

    cdef:
        char *data
        Py_ssize_t len
        char *format
        int ndim
        Py_ssize_t *shape
        Py_ssize_t *strides
        Py_ssize_t itemsize
        unicode mode
        bytes _format
        void (*callback_free_data)(char *data)

    def __cinit__(array self, tuple shape, Py_ssize_t itemsize, format,
                  mode=u"c", bint allocate_buffer=True):

        self.ndim = len(shape)
        self.itemsize = itemsize

        if not self.ndim:
            raise ValueError("Empty shape tuple for cython.array")

        if self.itemsize <= 0:
            raise ValueError("itemsize <= 0 for cython.array")

        encode = getattr(format, 'encode', None)
        if encode:
            format = encode('ASCII')
        self._format = format
        self.format = self._format

        self.shape = <Py_ssize_t *> malloc(sizeof(Py_ssize_t)*self.ndim)
        self.strides = <Py_ssize_t *> malloc(sizeof(Py_ssize_t)*self.ndim)

        if not self.shape or not self.strides:
            raise MemoryError("unable to allocate shape or strides.")

        cdef int idx
        # cdef Py_ssize_t dim, stride
        idx = 0
        for dim in shape:
            if dim <= 0:
                raise ValueError("Invalid shape.")

            self.shape[idx] = dim
            idx += 1

        stride = itemsize
        if mode == "fortran":
            idx = 0
            for dim in shape:
                self.strides[idx] = stride
                stride = stride * dim
                idx += 1
        elif mode == "c":
            idx = self.ndim-1
            for dim in shape[::-1]:
                self.strides[idx] = stride
                stride = stride * dim
                idx -= 1
        else:
            raise ValueError("Invalid mode, expected 'c' or 'fortran', got %s" % mode)

        self.len = stride

        decode = getattr(mode, 'decode', None)
        if decode:
            mode = decode('ASCII')
        self.mode = mode

        if allocate_buffer:
            self.data = <char *>malloc(self.len)
            if not self.data:
                raise MemoryError("unable to allocate array data.")

    def __getbuffer__(self, Py_buffer *info, int flags):

        cdef int bufmode = -1
        if self.mode == b"c":
            bufmode = PyBUF_C_CONTIGUOUS | PyBUF_ANY_CONTIGUOUS
        elif self.mode == b"fortran":
            bufmode = PyBUF_F_CONTIGUOUS | PyBUF_ANY_CONTIGUOUS
        if not (flags & bufmode):
            raise ValueError("Can only create a buffer that is contiguous in memory.")
        info.buf = self.data
        info.len = self.len
        info.ndim = self.ndim
        info.shape = self.shape
        info.strides = self.strides
        info.suboffsets = NULL
        info.itemsize = self.itemsize

        if flags & PyBUF_FORMAT:
            info.format = self.format
        else:
            info.format = NULL

        # we do not need to call releasebuffer
        info.obj = None

    def __releasebuffer__(array self, Py_buffer* info):
        # array.__releasebuffer__ should not be called,
        # because the Py_buffer's 'obj' field is set to None.
        raise NotImplementedError()

    def __dealloc__(array self):
        if self.data:
            if self.callback_free_data != NULL:
                self.callback_free_data(self.data)
            else:
                free(self.data)
            self.data = NULL
        if self.strides:
            free(self.strides)
            self.strides = NULL
        if self.shape:
            free(self.shape)
            self.shape = NULL
        self.format = NULL
        self.itemsize = 0

    def __getitem__(self, index):
        view = __pyx_memoryview_new(self, PyBUF_ANY_CONTIGUOUS|PyBUF_FORMAT)
        return view[index]

    def __setitem__(self, index, value):
        view = __pyx_memoryview_new(self, PyBUF_ANY_CONTIGUOUS|PyBUF_FORMAT)
        view[index] = value


@cname("__pyx_array_new")
cdef array array_cwrapper(tuple shape, Py_ssize_t itemsize, char *format, char *mode):
    return array(shape, itemsize, format, mode.decode('ASCII'))

########## View.MemoryView ##########

# from cpython cimport ...
cdef extern from "Python.h":
    int PyIndex_Check(object)

cdef extern from "pythread.h":
    ctypedef void *PyThread_type_lock

    PyThread_type_lock PyThread_allocate_lock()
    void PyThread_free_lock(PyThread_type_lock)
    int PyThread_acquire_lock(PyThread_type_lock, int mode) nogil
    void PyThread_release_lock(PyThread_type_lock) nogil

cdef extern from *:
    int __Pyx_GetBuffer(object, Py_buffer *, int)
    void __Pyx_ReleaseBuffer(Py_buffer *)

    ctypedef struct {{memviewslice_name}}:
        char *data
        Py_ssize_t shape[{{max_dims}}]
        Py_ssize_t strides[{{max_dims}}]
        Py_ssize_t suboffsets[{{max_dims}}]


@cname('__pyx_MemviewEnum')
cdef class Enum(object):
    cdef object name
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

cdef generic = Enum("<strided and direct or indirect>")
cdef strided = Enum("<strided and direct>") # default
cdef indirect = Enum("<strided and indirect>")
cdef generic_contiguous = Enum("<contiguous and direct or indirect>")
cdef contiguous = Enum("<contiguous and direct>")
cdef indirect_contiguous = Enum("<contiguous and indirect>")

# 'follow' is implied when the first or last axis is ::1

@cname('__pyx_memoryview')
cdef class memoryview(object):

    cdef object obj
    cdef Py_buffer view
    cdef PyThread_type_lock lock
    cdef int acquisition_count


    def __cinit__(memoryview self, object obj, int flags):
        self.obj = obj
        __Pyx_GetBuffer(obj, &self.view, flags)

        self.lock = PyThread_allocate_lock()
        if self.lock == NULL:
            raise MemoryError

    def __dealloc__(memoryview self):
        __Pyx_ReleaseBuffer(&self.view)
        PyThread_free_lock(self.lock)

    @cname('__pyx_memoryview_getitem')
    def __getitem__(memoryview self, object index):
        # cdef Py_ssize_t idx
        cdef char *itemp = <char *> self.view.buf
        cdef bytes bytesitem
        cdef str fmt = self.view.format

        import struct
        try:
            itemsize = struct.calcsize(fmt)
        except struct.error:
            raise TypeError("Unsupported format: %r" % fmt)

        if index is Ellipsis:
            return self

        elif isinstance(index, slice):
            if index == slice(None):
                return self

            raise NotImplementedError

        else:
            if not isinstance(index, tuple):
                index = (index,)

            tup = _unellipsify(index, self.view.ndim)

            if len(tup) != self.view.ndim:
                raise NotImplementedError(
                        "Expected %d indices (got %d)" %
                             (self.view.ndim, len(tup)))

            for dim, idx in enumerate(tup):
                _check_index(idx)
                itemp = pybuffer_index(&self.view, itemp, idx, dim + 1)

        # Do a manual and complete check here instead of this easy hack
        bytesitem = itemp[:self.view.itemsize]
        return struct.unpack(fmt, bytesitem)


@cname('__pyx_memoryviewslice')
cdef class _memoryviewslice(memoryview):
    "Internal class for passing memory view slices to Python"

    # We need this to keep our shape/strides/suboffset pointers valid
    cdef {{memviewslice_name}} from_slice
    # Restore the original Py_buffer before releasing
    cdef Py_buffer orig_view

    def __cinit__(self, object obj, int flags):
        self.orig_view = self.view

    def __dealloc__(self):
        self.view = self.orig_view


@cname('__pyx_memoryview_new')
cdef memoryview_cwrapper(object o, int flags):
    return memoryview(o, flags)

@cname('__pyx_memoryview_fromslice')
cdef memoryview memoryview_from_memview_cwrapper(memoryview m,  int flags,
                        int new_ndim, {{memviewslice_name}} *memviewslice):
    cdef _memoryviewslice result = _memoryviewslice(m.obj, flags)

    result.from_slice = memviewslice[0]

    result.view.shape = <Py_ssize_t *> (&result.from_slice.shape + new_ndim)
    result.view.strides = <Py_ssize_t *> (&result.from_slice.strides + new_ndim)
    result.view.suboffsets = <Py_ssize_t *> (&result.from_slice.suboffsets + new_ndim)
    result.view.ndim = new_ndim

    return result

cdef _check_index(index):
    if not PyIndex_Check(index):
        raise TypeError("Cannot index with %s" % type(index))

cdef tuple _unellipsify(tuple tup, int ndim):
    if Ellipsis in tup:
        result = []
        for idx, item in enumerate(tup):
            if item is Ellipsis:
                result.extend([slice(None)] * (ndim - len(tup) + 1))
                result.extend(tup[idx + 1:])
                break

            result.append(item)

        return tuple(result)

    return tup

@cname('__pyx_pybuffer_index')
cdef char *pybuffer_index(Py_buffer *view, char *bufp, Py_ssize_t index, int dim) except NULL:
    cdef Py_ssize_t shape, stride, suboffset = -1
    cdef Py_ssize_t itemsize = view.itemsize
    cdef char *resultp

    if view.ndim == 0:
        shape = view.len / itemsize
        stride = itemsize
    else:
        shape = view.shape[dim]
        stride = view.strides[dim]
        if view.suboffsets != NULL:
            suboffset = view.suboffsets[dim]

    if index < 0:
        index += view.shape[dim]
        if index < 0:
            raise IndexError("Out of bounds in dimension %d" % dim)

    if index > shape:
        raise IndexError("Out of bounds in dimension %d" % dim)

    resultp = bufp + index * stride

    if suboffset >= 0:
        resultp = (<char **> resultp)[0] + suboffset

    return resultp
