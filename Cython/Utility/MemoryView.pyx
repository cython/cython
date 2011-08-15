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
            free(self.shape)
            free(self.strides)
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

        # info.obj = self

    def __releasebuffer__(self, Py_buffer *info):
        pass

    def __dealloc__(array self):
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
cdef array array_cwrapper(tuple shape, Py_ssize_t itemsize, char *format, char *mode, char *buf):
    cdef array result
    if buf == NULL:
        result = array(shape, itemsize, format, mode.decode('ASCII'))
    else:
        result = array(shape, itemsize, format, mode.decode('ASCII'), allocate_buffer=False)
        result.data = buf

    return result

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
    int __Pyx_GetBuffer(object, Py_buffer *, int) except -1
    void __Pyx_ReleaseBuffer(Py_buffer *)

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
    cdef PyThread_type_lock lock
    cdef int acquisition_count
    cdef Py_buffer view

    def __cinit__(memoryview self, object obj, int flags):
        self.obj = obj

        if type(self) is memoryview or obj is not None:
            __Pyx_GetBuffer(obj, &self.view, flags)

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
            _check_index(idx)
            itemp = pybuffer_index(&self.view, itemp, idx, dim)

        return itemp

    @cname('__pyx_memoryview_getitem')
    def __getitem__(memoryview self, object index):
        if index is Ellipsis:
            return self

        have_slices, index = _unellipsify(index, self.view.ndim)

        cdef char *itemp
        if have_slices:
            return pybuffer_slice(self, index)
        else:
            itemp = self.get_item_pointer(index)
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
        result = struct.unpack(self.view.format, bytesitem)
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

    property T:
        @cname('__pyx_memoryview_transpose')
        def __get__(self):
            cdef memoryview result = memoryview_copy(self)

            cdef int ndim = self.view.ndim
            cdef Py_ssize_t *strides = result.view.strides
            cdef Py_ssize_t *shape = result.view.shape

            # reverse strides and shape
            for i in range(ndim / 2):
                strides[i], strides[ndim - i] = strides[ndim - i], strides[i]
                shape[i], shape[ndim - i] = shape[ndim - i], shape[i]

            return result

    property _obj:
        @cname('__pyx_memoryview__get__obj')
        def __get__(self):
            if (self.obj is None and <PyObject *> self.view.obj != NULL and
                    self.view.obj is not None):
                return <object> self.view.obj

            return self.obj

    property shape:
        @cname('__pyx_memoryview_get_shape')
        def __get__(self):
            return tuple([self.view.shape[i] for i in xrange(self.view.ndim)])


    property strides:
        @cname('__pyx_memoryview_get_strides')
        def __get__(self):
            return tuple([self.view.strides[i] for i in xrange(self.view.ndim)])


    property suboffsets:
        @cname('__pyx_memoryview_get_suboffsets')
        def __get__(self):
            return tuple([self.view.suboffsets[i] for i in xrange(self.view.ndim)])

    def __repr__(self):
        return "<MemoryView of %r at 0x%x>" % (self._obj.__class__.__name__, id(self))

    def __str__(self):
        return "<MemoryView of %r object>" % (self._obj.__class__.__name__,)


@cname('__pyx_memoryview_new')
cdef memoryview_cwrapper(object o, int flags):
    return memoryview(o, flags)


cdef _check_index(index):
    if not PyIndex_Check(index):
        raise TypeError("Cannot index with %s" % type(index))

cdef tuple _unellipsify(object index, int ndim):
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
                result.extend(tup[idx + 1:])
            else:
                result.append(slice(None))
            have_slices = True
        else:
            have_slices = have_slices or isinstance(item, slice)
            result.append(item)

    nslices = ndim - len(result)
    if nslices:
        result.extend([slice(None)] * nslices)

    for idx in tup:
        if isinstance(idx, slice):
            return True, tup

    return False, tup

@cname('__pyx_pybuffer_slice')
cdef memoryview pybuffer_slice(memoryview memview, object indices):
    cdef Py_ssize_t idx, dim, new_dim = 0, suboffset_dim = -1
    cdef Py_ssize_t shape, stride
    cdef bint negative_step
    cdef int new_ndim = 0
    cdef {{memviewslice_name}} dst

    for dim, index in enumerate(indices):
        shape = memview.view.shape[dim]
        stride = memview.view.strides[dim]

        if PyIndex_Check(index):
            idx = index
            if idx < 0:
                idx += shape
            if not 0 <= idx < shape:
                raise IndexError("Index out of bounds (axis %d)" % dim)
        else:
            # index is a slice
            new_ndim += 1

            start, stop, step = index.start, index.stop, index.step
            negative_step = step and step < 0

            # set some defaults
            if not start:
                if negative_step:
                    start = shape - 1
                else:
                    start = 0

            if not stop:
                if negative_step:
                    stop = -1
                else:
                    stop = shape

            # check our bounds
            if start < 0:
                start += shape
                if start < 0:
                    start = 0
            elif start >= shape:
                start = shape - 1

            if stop < 0:
                stop += shape
                if stop < 0:
                    stop = 0
            elif stop > shape:
                stop = shape

            step = step or 1

            # shape/strides/suboffsets
            dst.strides[new_dim] = stride * step
            dst.shape[new_dim] = (stop - start) / step
            if (stop - start) % step:
                dst.shape[new_dim] += 1
            dst.suboffsets[new_dim] = memview.view.suboffsets[dim]

            # set this for the slicing offset
            if negative_step:
                idx = stop
            else:
                idx = start

        # Add the slicing or idexing offsets to the right suboffset or base data *
        if suboffset_dim < 0:
            dst.data += idx * stride
        else:
            dst.suboffsets[suboffset_dim] += idx * stride

        if memview.view.suboffsets[dim]:
            if PyIndex_Check(index):
                raise IndexError(
                    "Cannot make indirect dimension %d disappear through "
                    "indexing, consider slicing with %d:%d" % (dim, idx, idx + 1))
            suboffset_dim = new_dim

    cdef _memoryviewslice memviewsliceobj
    if isinstance(memview, _memoryviewslice):
        memviewsliceobj = memview
        return memoryview_fromslice(&dst, new_dim,
                                    memviewsliceobj.to_object_func,
                                    memviewsliceobj.to_dtype_func)
    else:
        return memoryview_fromslice(&dst, new_dim, NULL, NULL)

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

@cname('__pyx_memoryviewslice')
cdef class _memoryviewslice(memoryview):
    "Internal class for passing memory view slices to Python"

    # We need this to keep our shape/strides/suboffset pointers valid
    cdef {{memviewslice_name}} from_slice
    # We need this only to print it's classes name
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

    property _obj:
        @cname('__pyx_memoryviewslice__get__obj')
        def __get__(self):
            return self.from_object


@cname('__pyx_memoryview_fromslice')
cdef memoryview_fromslice({{memviewslice_name}} *memviewslice,
                          int ndim,
                          object (*to_object_func)(char *),
                          int (*to_dtype_func)(char *, object) except 0):

    assert 0 < ndim <= memviewslice.memview.view.ndim, (ndim, memviewslice.memview.view.ndim)

    cdef _memoryviewslice result = _memoryviewslice(None, 0)

    result.from_slice = memviewslice[0]
    __PYX_INC_MEMVIEW(memviewslice, 1)

    result.from_object = <object> memviewslice.memview.obj

    result.view = memviewslice.memview.view
    result.view.shape = <Py_ssize_t *> &result.from_slice.shape
    result.view.strides = <Py_ssize_t *> result.from_slice.strides
    result.view.suboffsets = <Py_ssize_t *> &result.from_slice.suboffsets
    result.view.ndim = ndim

    result.to_object_func = to_object_func
    result.to_dtype_func = to_dtype_func

    return result

cdef memoryview_copy(memoryview memview):
    cdef {{memviewslice_name}} memviewslice
    cdef int dim
    cdef object (*to_object_func)(char *)
    cdef int (*to_dtype_func)(char *, object) except 0

    memviewslice.memview = <__pyx_memoryview *> memview
    memviewslice.data = <char *> memview.view.buf

    # Copy all of these as from_slice will
    for dim in range(memview.view.ndim):
        memviewslice.shape[dim] = memview.view.shape[dim]
        memviewslice.strides[dim] = memview.view.strides[dim]
        memviewslice.suboffsets[dim] = memview.view.suboffsets[dim]

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

    ctypedef struct __Pyx_TypeInfo:
      char* name
      __Pyx_StructField* fields
      size_t size
      char typegroup
      char is_unsigned

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

        parts = ["T{"]
        field = type.fields

        while field.type:
            parts.append(format_from_typeinfo(field.type))
            field += 1

        parts.append("}")
        result = "".join(parts)
    else:
        fmt = __Pyx_TypeInfoToFormat(type)
        result = fmt.string

    return result
