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
        PyBUF_WRITABLE


    void Py_INCREF(object)
    void Py_DECREF(object)

cdef extern from *:
    object __pyx_memoryview_new(object obj, int flags)

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
        unicode mode
        bytes _format
        void (*callback_free_data)(void *data)
        # cdef object _memview
        cdef bint free_data

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

        self._shape = <Py_ssize_t *> malloc(sizeof(Py_ssize_t)*self.ndim)
        self._strides = <Py_ssize_t *> malloc(sizeof(Py_ssize_t)*self.ndim)

        if not self._shape or not self._strides:
            free(self._shape)
            free(self._strides)
            raise MemoryError("unable to allocate shape or strides.")

        cdef int idx
        # cdef Py_ssize_t dim, stride
        idx = 0
        for dim in shape:
            if dim <= 0:
                raise ValueError("Invalid shape.")

            self._shape[idx] = dim
            idx += 1

        stride = itemsize
        if mode == "fortran":
            idx = 0
            for dim in shape:
                self._strides[idx] = stride
                stride = stride * dim
                idx += 1
        elif mode == "c":
            idx = self.ndim-1
            for dim in shape[::-1]:
                self._strides[idx] = stride
                stride = stride * dim
                idx -= 1
        else:
            raise ValueError("Invalid mode, expected 'c' or 'fortran', got %s" % mode)

        self.len = stride

        decode = getattr(mode, 'decode', None)
        if decode:
            mode = decode('ASCII')
        self.mode = mode

        self.free_data = allocate_buffer
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
        info.shape = self._shape
        info.strides = self._strides
        info.suboffsets = NULL
        info.itemsize = self.itemsize
        info.readonly = 0

        if flags & PyBUF_FORMAT:
            info.format = self.format
        else:
            info.format = NULL

        info.obj = self

    def __dealloc__(array self):
        if self.callback_free_data != NULL:
            self.callback_free_data(self.data)
        elif self.free_data:
            free(self.data)

        self.data = NULL

        if self._strides:
            free(self._strides)
            self._strides = NULL

        if self._shape:
            free(self._shape)
            self._shape = NULL

        self.format = NULL
        self.itemsize = 0

    property memview:
        @cname('__pyx_cython_array_get_memview')
        def __get__(self):
            # Make this a property as 'data' may be set after instantiation
            #if self._memview is None:
            #    flags = PyBUF_ANY_CONTIGUOUS|PyBUF_FORMAT|PyBUF_WRITABLE
            #    self._memview = __pyx_memoryview_new(self, flags)

            #return self._memview
            flags =  PyBUF_ANY_CONTIGUOUS|PyBUF_FORMAT|PyBUF_WRITABLE
            return  __pyx_memoryview_new(self, flags)


    def __getattr__(self, attr):
        return getattr(self.memview, attr)

    def __getitem__(self, item):
        return self.memview[item]

    def __setitem__(self, item, value):
        self.memview[item] = value


@cname("__pyx_array_new")
cdef array array_cwrapper(tuple shape, Py_ssize_t itemsize, char *format, char *mode, char *buf):
    cdef array result
    if buf == NULL:
        result = array(shape, itemsize, format, mode.decode('ASCII'))
    else:
        result = array(shape, itemsize, format, mode.decode('ASCII'), allocate_buffer=False)
        result.data = buf

    return result

#################### View.MemoryView ####################

import cython

# from cpython cimport ...
cdef extern from "Python.h":
    int PyIndex_Check(object)
    object PyLong_FromVoidPtr(void *)

cdef extern from "pythread.h":
    ctypedef void *PyThread_type_lock

    PyThread_type_lock PyThread_allocate_lock()
    void PyThread_free_lock(PyThread_type_lock)
    int PyThread_acquire_lock(PyThread_type_lock, int mode) nogil
    void PyThread_release_lock(PyThread_type_lock) nogil

cdef extern from "string.h":
    void *memset(void *b, int c, size_t len)

cdef extern from *:
    int __Pyx_GetBuffer(object, Py_buffer *, int) except -1
    void __Pyx_ReleaseBuffer(Py_buffer *)

    void Py_INCREF(object)
    void Py_DECREF(object)
    void Py_XINCREF(object)

    ctypedef struct PyObject

    cdef struct __pyx_memoryview "__pyx_memoryview_obj":
        Py_buffer view
        PyObject *obj

    ctypedef struct {{memviewslice_name}}:
        __pyx_memoryview *memview
        char *data
        Py_ssize_t shape[{{max_dims}}]
        Py_ssize_t strides[{{max_dims}}]
        Py_ssize_t suboffsets[{{max_dims}}]

    void __PYX_INC_MEMVIEW({{memviewslice_name}} *memslice, int have_gil)
    void __PYX_XDEC_MEMVIEW({{memviewslice_name}} *memslice, int have_gil)

    ctypedef struct __pyx_buffer "Py_buffer":
        PyObject *obj

    PyObject *Py_None

    cdef enum:
        PyBUF_C_CONTIGUOUS,
        PyBUF_F_CONTIGUOUS,
        PyBUF_ANY_CONTIGUOUS
        PyBUF_FORMAT
        PyBUF_WRITABLE
        PyBUF_STRIDES
        PyBUF_INDIRECT

@cname('__pyx_MemviewEnum')
cdef class Enum(object):
    cdef object name
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

# Disable generic_contiguous, as it makes trouble verifying contiguity:
#   - 'contiguous' or '::1' means the dimension is contiguous with dtype
#   - 'indirect_contiguous' means a contiguous list of pointers
#   - dtype contiguous must be contiguous in the first or last dimension
#     from the start, or from the dimension following the last indirect dimension
#
#   e.g.
#           int[::indirect_contiguous, ::contiguous, :]
#
#   is valid (list of pointers to 2d fortran-contiguous array), but
#
#           int[::generic_contiguous, ::contiguous, :]
#
#   would mean you'd have assert dimension 0 to be indirect (and pointer contiguous) at runtime.
#   So it doesn't bring any performance benefit, and it's only confusing.

cdef generic = Enum("<strided and direct or indirect>")
cdef strided = Enum("<strided and direct>") # default
cdef indirect = Enum("<strided and indirect>")
# Disable generic_contiguous, as it is a troublemaker
#cdef generic_contiguous = Enum("<contiguous and direct or indirect>")
cdef contiguous = Enum("<contiguous and direct>")
cdef indirect_contiguous = Enum("<contiguous and indirect>")

# 'follow' is implied when the first or last axis is ::1

@cname('__pyx_memoryview')
cdef class memoryview(object):

    cdef object obj
    cdef object _size
    cdef object _array_interface
    cdef PyThread_type_lock lock
    cdef int acquisition_count
    cdef Py_buffer view
    cdef int flags

    def __cinit__(memoryview self, object obj, int flags):
        self.obj = obj

        if type(self) is memoryview or obj is not None:
            __Pyx_GetBuffer(obj, &self.view, flags)
            if <PyObject *> self.view.obj == NULL:
                (<__pyx_buffer *> &self.view).obj = Py_None
                Py_INCREF(None)

        self.lock = PyThread_allocate_lock()
        if self.lock == NULL:
            raise MemoryError

    def __dealloc__(memoryview self):
        if self.obj is not None:
            __Pyx_ReleaseBuffer(&self.view)

        if self.lock != NULL:
            PyThread_free_lock(self.lock)

    cdef char *get_item_pointer(memoryview self, object index) except NULL:
        cdef Py_ssize_t dim
        cdef char *itemp = <char *> self.view.buf

        for dim, idx in enumerate(index):
            itemp = pybuffer_index(&self.view, itemp, idx, dim)

        return itemp

    @cname('__pyx_memoryview_getitem')
    def __getitem__(memoryview self, object index):
        if index is Ellipsis:
            return self

        have_slices, indices = _unellipsify(index, self.view.ndim)

        cdef char *itemp
        if have_slices:
            return memview_slice(self, indices)
        else:
            itemp = self.get_item_pointer(indices)
            return self.convert_item_to_object(itemp)

    @cname('__pyx_memoryview_setitem')
    def __setitem__(memoryview self, object index, object value):
        have_slices, index = _unellipsify(index, self.view.ndim)
        if have_slices:
            raise NotImplementedError("Slice assignment not supported yet")

        cdef char *itemp = self.get_item_pointer(index)
        self.assign_item_from_object(itemp, value)

    cdef convert_item_to_object(self, char *itemp):
        """Only used if instantiated manually by the user, or if Cython doesn't
        know how to convert the type"""
        import struct
        cdef bytes bytesitem
        # Do a manual and complete check here instead of this easy hack
        bytesitem = itemp[:self.view.itemsize]
        try:
            result = struct.unpack(self.view.format, bytesitem)
        except struct.error:
            raise ValueError("Unable to convert item to object")
        else:
            if len(self.view.format) == 1:
                return result[0]
            return result

    cdef assign_item_from_object(self, char *itemp, object value):
        """Only used if instantiated manually by the user, or if Cython doesn't
        know how to convert the type"""
        import struct
        cdef char c
        cdef bytes bytesvalue
        cdef Py_ssize_t i

        if isinstance(value, tuple):
            bytesvalue = struct.pack(self.view.format, *value)
        else:
            bytesvalue = struct.pack(self.view.format, value)

        for i, c in enumerate(bytesvalue):
            itemp[i] = c

    def __getbuffer__(self, Py_buffer *info, int flags):
        if flags & PyBUF_STRIDES:
            info.shape = self.view.shape
        else:
            info.shape = NULL

        if flags & PyBUF_STRIDES:
            info.strides = self.view.strides
        else:
            info.strides = NULL

        if flags & PyBUF_INDIRECT:
            info.suboffsets = self.view.suboffsets
        else:
            info.suboffsets = NULL

        if flags & PyBUF_FORMAT:
            info.format = self.view.format
        else:
            info.format = NULL

        info.buf = self.view.buf
        info.ndim = self.view.ndim
        info.itemsize = self.view.itemsize
        info.len = self.view.len
        info.readonly = 0
        info.obj = self


    # Some properties that have the same sematics as in NumPy
    property T:
        @cname('__pyx_memoryview_transpose')
        def __get__(self):
            cdef _memoryviewslice result = memoryview_copy(self)
            transpose_memslice(&result.from_slice)
            return result

    property base:
        @cname('__pyx_memoryview__get__base')
        def __get__(self):
            return self.obj

    property shape:
        @cname('__pyx_memoryview_get_shape')
        def __get__(self):
            return tuple([self.view.shape[i] for i in xrange(self.view.ndim)])

    property strides:
        @cname('__pyx_memoryview_get_strides')
        def __get__(self):
            if self.view.strides == NULL:
                # Note: we always ask for strides, so if this is not set it's a bug
                raise ValueError("Buffer view does not expose strides")

            return tuple([self.view.strides[i] for i in xrange(self.view.ndim)])

    property suboffsets:
        @cname('__pyx_memoryview_get_suboffsets')
        def __get__(self):
            if self.view.suboffsets == NULL:
                return [-1] * self.view.ndim

            return tuple([self.view.suboffsets[i] for i in xrange(self.view.ndim)])

    property ndim:
        @cname('__pyx_memoryview_get_ndim')
        def __get__(self):
            return self.view.ndim

    property itemsize:
        @cname('__pyx_memoryview_get_itemsize')
        def __get__(self):
            return self.view.itemsize

    property nbytes:
        @cname('__pyx_memoryview_get_nbytes')
        def __get__(self):
            return self.size * self.view.itemsize

    property size:
        @cname('__pyx_memoryview_get_size')
        def __get__(self):
            if self._size is None:
                result = 1

                for length in self.shape:
                    result *= length

                self._size = result

            return self._size

    # The __array_interface__ is broken as it does not properly convert PEP 3118 format
    # strings into NumPy typestrs. NumPy 1.5 support the new buffer interface though.
    '''
    property __array_interface__:
        @cname('__pyx_numpy_array_interface')
        def __get__(self):
            "Interface for NumPy to obtain a ndarray from this object"
            # Note: we always request writable buffers, so we set readonly to
            # False in the data tuple
            if self._array_interface is None:
                for suboffset in self.suboffsets:
                    if suboffset >= 0:
                        raise ValueError("Cannot convert indirect buffer to numpy object")

                self._array_interface = dict(
                    data = (PyLong_FromVoidPtr(self.view.buf), False),
                    shape = self.shape,
                    strides = self.strides,
                    typestr = "%s%d" % (self.view.format, self.view.itemsize),
                    version = 3)

            return self._array_interface
    '''

    def __len__(self):
        if self.view.ndim >= 1:
            return self.view.shape[0]

        return 0

    def __repr__(self):
        return "<MemoryView of %r at 0x%x>" % (self.base.__class__.__name__, id(self))

    def __str__(self):
        return "<MemoryView of %r object>" % (self.base.__class__.__name__,)


@cname('__pyx_memoryview_new')
cdef memoryview_cwrapper(object o, int flags):
    return memoryview(o, flags)

cdef tuple _unellipsify(object index, int ndim):
    """
    Replace all ellipses with full slices and fill incomplete indices with
    full slices.
    """
    if not isinstance(index, tuple):
        tup = (index,)
    else:
        tup = index

    result = []
    have_slices = False
    seen_ellipsis = False
    for idx, item in enumerate(tup):
        if item is Ellipsis:
            if not seen_ellipsis:
                result.extend([slice(None)] * (ndim - len(tup) + 1))
                seen_ellipsis = True
            else:
                result.append(slice(None))
            have_slices = True
        else:
            if not isinstance(item, slice) and not PyIndex_Check(item):
                raise TypeError("Cannot index with type '%s'" % type(item))

            have_slices = have_slices or isinstance(item, slice)
            result.append(item)

    nslices = ndim - len(result)
    if nslices:
        result.extend([slice(None)] * nslices)

    return have_slices or nslices, tuple(result)

#
### Slicing a memoryview
#

@cname('__pyx_memview_slice')
cdef memoryview memview_slice(memoryview memview, object indices):
    cdef int new_ndim = 0, suboffset_dim = -1, dim
    cdef bint negative_step
    cdef {{memviewslice_name}} src, dst
    cdef {{memviewslice_name}} *p_src

    # dst is copied by value in memoryview_fromslice -- initialize it
    # src is never copied
    memset(&dst, 0, sizeof(dst))

    cdef _memoryviewslice memviewsliceobj

    assert memview.view.ndim > 0

    if isinstance(memview, _memoryviewslice):
        memviewsliceobj = memview
        p_src = &memviewsliceobj.from_slice
    else:
        slice_copy(memview, &src)
        p_src = &src

    # Note: don't use variable src at this point
    # SubNote: we should be able to declare variables in blocks...

    # memoryview_fromslice() will inc our dst slice
    dst.memview = p_src.memview
    dst.data = p_src.data

    # Put everything in temps to avoid this bloody warning:
    # "Argument evaluation order in C function call is undefined and
    #  may not be as expected"
    cdef {{memviewslice_name}} *p_dst = &dst
    cdef int *p_suboffset_dim = &suboffset_dim
    cdef Py_ssize_t start, stop, step
    cdef bint have_start, have_stop, have_step

    for dim, index in enumerate(indices):
        if PyIndex_Check(index):
            slice_memviewslice(p_src, p_dst, True, dim, new_ndim, p_suboffset_dim,
                               index, 0, 0, 0, 0, 0, False)
        else:
            start = index.start or 0
            stop = index.stop or 0
            step = index.step or 0

            have_start = index.start is not None
            have_stop = index.stop is not None
            have_step = index.step is not None

            slice_memviewslice(p_src, p_dst, True, dim, new_ndim, p_suboffset_dim,
                               start, stop, step, have_start, have_stop, have_step,
                               True)
            new_ndim += 1

    if isinstance(memview, _memoryviewslice):
        return memoryview_fromslice(&dst, new_ndim,
                                    memviewsliceobj.to_object_func,
                                    memviewsliceobj.to_dtype_func)
    else:
        return memoryview_fromslice(&dst, new_ndim, NULL, NULL)


#
### Slicing in a single dimension of a memoryviewslice
#

cdef extern from "stdlib.h":
    void abort() nogil
    void printf(char *s, ...) nogil

cdef extern from "stdio.h":
    ctypedef struct FILE
    FILE *stderr
    int fputs(char *s, FILE *stream)

cdef extern from "pystate.h":
    void PyThreadState_Get() nogil

    # These are not actually nogil, but we check for the GIL before calling them
    void PyErr_SetString(PyObject *type, char *msg) nogil
    PyObject *PyErr_Format(PyObject *exc, char *msg, ...) nogil

@cname('__pyx_memoryview_slice_memviewslice')
cdef char *slice_memviewslice({{memviewslice_name}} *src,
                              {{memviewslice_name}} *dst,
                              bint have_gil,
                              int dim,
                              int new_ndim,
                              int *suboffset_dim,
                              Py_ssize_t start,
                              Py_ssize_t stop,
                              Py_ssize_t step,
                              int have_start,
                              int have_stop,
                              int have_step,
                              bint is_slice) nogil except *:
    """
    Create a new slice dst given slice src.

    have_gil        - if true, the GIL must be held and exceptions may be raised
    dim             - the current src dimension (indexing will make dimensions
                                                 disappear)
    new_dim         - the new dst dimension
    suboffset_dim   - pointer to a single int initialized to -1 to keep track of
                      where slicing offsets should be added
    """

    cdef:
        Py_ssize_t shape, stride, suboffset
        Py_ssize_t new_shape
        bint negative_step

        # Somehow these pointers are NULL when set as globals... this needs investigation
        char *ERR_OOB = "Index out of bounds (axis %d)"
        char *ERR_STEP = "Step must not be zero (axis %d)"
        char *ERR_INDIRECT_GIL = ("Cannot make indirect dimension %d disappear "
                              "through indexing, consider slicing with %d:%d")
        char *ERR_INDIRECT_NOGIL = ("Cannot make indirect dimension %d disappear "
                                "through indexing")
        PyObject *exc = <PyObject *> IndexError

    if have_gil:
        # Assert the GIL
        PyThreadState_Get()

    shape = src.shape[dim]
    stride = src.strides[dim]
    suboffset = src.suboffsets[dim]

    if not is_slice:
        # index is a normal integer-like index
        if start < 0:
            start += shape
        if not 0 <= start < shape:
            if have_gil:
                PyErr_Format(exc, ERR_OOB, dim)
            return ERR_OOB
    else:
        # index is a slice
        negative_step = have_step != 0 and step < 0

        if have_step and step == 0:
            if have_gil:
                # ValueError might be more appropriate, but this will make it consistent
                # with nogil slicing
                PyErr_SetString(exc, ERR_STEP)
            return ERR_STEP

        # check our bounds and set defaults
        if have_start:
            if start < 0:
                start += shape
                if start < 0:
                    start = 0
            elif start >= shape:
                if negative_step:
                    start = shape - 1
                else:
                    start = shape
        else:
            if negative_step:
                start = shape - 1
            else:
                start = 0

        if have_stop:
            if stop < 0:
                stop += shape
                if stop < 0:
                    stop = 0
            elif stop > shape:
                stop = shape
        else:
            if negative_step:
                stop = -1
            else:
                stop = shape

        if not have_step:
            step = 1

        # len = ceil( (stop - start) / step )
        with cython.cdivision(True):
            new_shape = (stop - start) // step

            if (stop - start) % step:
                new_shape += 1

        if new_shape < 0:
            new_shape = 0

        # shape/strides/suboffsets
        dst.strides[new_ndim] = stride * step
        dst.shape[new_ndim] = new_shape
        dst.suboffsets[new_ndim] = suboffset

    # Add the slicing or idexing offsets to the right suboffset or base data *
    if suboffset_dim[0] < 0:
        dst.data += start * stride
    else:
        dst.suboffsets[suboffset_dim[0]] += start * stride

    if suboffset >= 0:
        if not is_slice:
            if have_gil:
                PyErr_Format(exc, ERR_INDIRECT_GIL, dim, start, start + 1)
            return ERR_INDIRECT_NOGIL
        else:
            suboffset_dim[0] = new_ndim

    return NULL

#
### Index a memoryview
#
@cname('__pyx_pybuffer_index')
cdef char *pybuffer_index(Py_buffer *view, char *bufp, Py_ssize_t index,
                          int dim) except NULL:
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
            raise IndexError("Out of bounds on buffer access (axis %d)" % dim)

    if index >= shape:
        raise IndexError("Out of bounds on buffer access (axis %d)" % dim)

    resultp = bufp + index * stride
    if suboffset >= 0:
        resultp = (<char **> resultp)[0] + suboffset

    return resultp

#
### Transposing a memoryviewslice
#
@cname('__pyx_memslice_transpose')
cdef int transpose_memslice({{memviewslice_name}} *memslice) nogil except 0:
    cdef int ndim = memslice.memview.view.ndim

    cdef Py_ssize_t *shape = memslice.shape
    cdef Py_ssize_t *strides = memslice.strides

    # reverse strides and shape
    cdef int i, j
    for i in range(ndim / 2):
        j = ndim - 1 - i
        strides[i], strides[j] = strides[j], strides[i]
        shape[i], shape[j] = shape[j], shape[i]

        if memslice.suboffsets[i] >= 0 or memslice.suboffsets[j] >= 0:
            with gil:
                raise ValueError("Cannot transpose memoryview with indirect dimensions")

    return 1

#
### Creating new memoryview objects from slices and memoryviews
#
@cname('__pyx_memoryviewslice')
cdef class _memoryviewslice(memoryview):
    "Internal class for passing memoryview slices to Python"

    # We need this to keep our shape/strides/suboffset pointers valid
    cdef {{memviewslice_name}} from_slice
    # We need this only to print it's class' name
    cdef object from_object

    cdef object (*to_object_func)(char *)
    cdef int (*to_dtype_func)(char *, object) except 0

    def __dealloc__(self):
        __PYX_XDEC_MEMVIEW(&self.from_slice, 1)

    cdef convert_item_to_object(self, char *itemp):
        if self.to_object_func != NULL:
            return self.to_object_func(itemp)
        else:
            return memoryview.convert_item_to_object(self, itemp)

    cdef assign_item_from_object(self, char *itemp, object value):
        if self.to_dtype_func != NULL:
            self.to_dtype_func(itemp, value)
        else:
            memoryview.assign_item_from_object(self, itemp, value)

    property base:
        @cname('__pyx_memoryviewslice__get__base')
        def __get__(self):
            return self.from_object

@cname('__pyx_memoryview_fromslice')
cdef memoryview_fromslice({{memviewslice_name}} *memviewslice,
                          int ndim,
                          object (*to_object_func)(char *),
                          int (*to_dtype_func)(char *, object) except 0):

    cdef _memoryviewslice result
    cdef int i

    assert 0 < ndim <= memviewslice.memview.view.ndim, (ndim, memviewslice.memview.view.ndim)

    result = _memoryviewslice(None, 0)

    result.from_slice = memviewslice[0]
    __PYX_INC_MEMVIEW(memviewslice, 1)

    result.from_object = <object> memviewslice.memview.obj

    result.view = memviewslice.memview.view
    result.view.buf = <void *> memviewslice.data
    result.view.ndim = ndim
    (<__pyx_buffer *> &result.view).obj = Py_None
    Py_INCREF(None)

    result.view.shape = <Py_ssize_t *> result.from_slice.shape
    result.view.strides = <Py_ssize_t *> result.from_slice.strides
    result.view.suboffsets = <Py_ssize_t *> result.from_slice.suboffsets

    result.view.len = result.view.itemsize
    for i in range(ndim):
        result.view.len *= result.view.shape[i]

    result.to_object_func = to_object_func
    result.to_dtype_func = to_dtype_func

    return result

@cname('__pyx_memoryview_slice_copy')
cdef void slice_copy(memoryview memview, {{memviewslice_name}} *dst):
    cdef int dim

    dst.memview = <__pyx_memoryview *> memview
    dst.data = <char *> memview.view.buf

    for dim in range(memview.view.ndim):
        dst.shape[dim] = memview.view.shape[dim]
        dst.strides[dim] = memview.view.strides[dim]
        dst.suboffsets[dim] = memview.view.suboffsets[dim]

@cname('__pyx_memoryview_copy')
cdef memoryview_copy(memoryview memview):
    cdef {{memviewslice_name}} memviewslice
    cdef object (*to_object_func)(char *)
    cdef int (*to_dtype_func)(char *, object) except 0

    slice_copy(memview, &memviewslice)

    if isinstance(memview, _memoryviewslice):
        to_object_func = (<_memoryviewslice> memview).to_object_func
        to_dtype_func = (<_memoryviewslice> memview).to_dtype_func
    else:
        to_object_func = NULL
        to_dtype_func = NULL

    return memoryview_fromslice(&memviewslice, memview.view.ndim,
                                to_object_func, to_dtype_func)

############### BufferFormatFromTypeInfo ###############
cdef extern from *:
    ctypedef struct __Pyx_StructField

    cdef enum:
        __PYX_BUF_FLAGS_PACKED_STRUCT
        __PYX_BUF_FLAGS_INTEGER_COMPLEX

    ctypedef struct __Pyx_TypeInfo:
      char* name
      __Pyx_StructField* fields
      size_t size
      char typegroup
      char is_unsigned
      int flags

    ctypedef struct __Pyx_StructField:
      __Pyx_TypeInfo* type
      char* name
      size_t offset

    ctypedef struct __Pyx_BufFmt_StackElem:
      __Pyx_StructField* field
      size_t parent_offset

    #ctypedef struct __Pyx_BufFmt_Context:
    #  __Pyx_StructField root
      __Pyx_BufFmt_StackElem* head

    struct __pyx_typeinfo_string:
        char string[3]

    __pyx_typeinfo_string __Pyx_TypeInfoToFormat(__Pyx_TypeInfo *)


@cname('__pyx_format_from_typeinfo')
cdef format_from_typeinfo(__Pyx_TypeInfo *type):
    cdef __Pyx_StructField *field
    cdef __pyx_typeinfo_string fmt

    if type.typegroup == 'S':
        assert type.fields != NULL and type.fields.type != NULL

        if type.flags & __PYX_BUF_FLAGS_PACKED_STRUCT:
            alignment = '^'
        else:
            alignment = ''

        parts = ["T{"]
        field = type.fields

        while field.type:
            parts.append(format_from_typeinfo(field.type))
            field += 1

        result = alignment.join(parts) + '}'
    else:
        fmt = __Pyx_TypeInfoToFormat(type)
        result = fmt.string

    return result
