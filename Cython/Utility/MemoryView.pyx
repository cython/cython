#################### View.MemoryView ####################

# cython: language_level=3str
# cython: binding=False

# This utility provides cython.array and cython.view.memoryview

from __future__ import absolute_import

cimport cython

# from cpython cimport ...
extern from "Python.h":
    ctypedef struct PyObject
    fn i32 PyIndex_Check(object)
    PyObject *PyExc_IndexError
    PyObject *PyExc_ValueError

extern from "pythread.h":
    ctypedef void *PyThread_type_lock

    fn PyThread_type_lock PyThread_allocate_lock()
    fn void PyThread_free_lock(PyThread_type_lock)

extern from "<string.h>":
    fn void *memset(void *b, i32 c, usize len)

extern from *:
    fn bint __PYX_CYTHON_ATOMICS_ENABLED()
    fn i32 __Pyx_GetBuffer(object, Py_buffer *, i32) except -1
    fn void __Pyx_ReleaseBuffer(Py_buffer *)

    ctypedef struct PyObject
    ctypedef isize Py_intptr_t
    fn void Py_INCREF(PyObject *)
    fn void Py_DECREF(PyObject *)

    fn void* PyMem_Malloc(usize n)
    fn void PyMem_Free(void *p)
    fn void* PyObject_Malloc(usize n)
    fn void PyObject_Free(void *p)

    struct __pyx_memoryview "__pyx_memoryview_obj":
        Py_buffer view
        PyObject *obj
        __Pyx_TypeInfo *typeinfo

    ctypedef struct {{memviewslice_name}}:
        __pyx_memoryview *memview
        char *data
        isize shape[{{max_dims}}]
        isize strides[{{max_dims}}]
        isize suboffsets[{{max_dims}}]

    fn void __PYX_INC_MEMVIEW({{memviewslice_name}} *memslice, i32 have_gil)
    fn void __PYX_XCLEAR_MEMVIEW({{memviewslice_name}} *memslice, i32 have_gil)

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
        PyBUF_ND
        PyBUF_RECORDS
        PyBUF_RECORDS_RO

    ctypedef struct __Pyx_TypeInfo:
        pass

extern from *:
    ctypedef i32 __pyx_atomic_int_type
    {{memviewslice_name}} slice_copy_contig "__pyx_memoryview_copy_new_contig"(
                                 __Pyx_memviewslice *from_mvs,
                                 char *mode, i32 ndim,
                                 usize sizeof_dtype, i32 contig_flag,
                                 bint dtype_is_object) except * nogil
    fn bint slice_is_contig "__pyx_memviewslice_is_contig" (
                            {{memviewslice_name}} mvs, char order, i32 ndim) nogil
    fn bint slices_overlap "__pyx_slices_overlap" ({{memviewslice_name}} *slice1,
                                                {{memviewslice_name}} *slice2,
                                                i32 ndim, usize itemsize) nogil

extern from "<stdlib.h>":
    fn void *malloc(usize) nogil
    fn void free(void *) nogil
    fn void *memcpy(void *dest, void *src, usize n) nogil

# the sequence abstract base class
cdef object __pyx_collections_abc_Sequence "__pyx_collections_abc_Sequence"
try:
    if __import__("sys").version_info >= (3, 3):
        __pyx_collections_abc_Sequence = __import__("collections.abc").abc.Sequence
    else:
        __pyx_collections_abc_Sequence = __import__("collections").Sequence
except:
    # it isn't a big problem if this fails
    __pyx_collections_abc_Sequence = None

#
### cython.array class
#

@cython.collection_type("sequence")
@cname("__pyx_array")
cdef class array:

    cdef:
        char *data
        isize len
        char *format
        i32 ndim
        isize *_shape
        isize *_strides
        isize itemsize
        unicode mode  # FIXME: this should have been a simple 'char'
        bytes _format
        void (*callback_free_data)(void *data) noexcept
        # cdef object _memview
        cdef bint free_data
        cdef bint dtype_is_object

    def __cinit__(array self, tuple shape, isize itemsize, format not None,
                  mode="c", bint allocate_buffer=true):
        let i32 idx
        let isize dim

        self.ndim = <i32>len(shape)
        self.itemsize = itemsize

        if not self.ndim:
            raise ValueError, "Empty shape tuple for cython.array"

        if itemsize <= 0:
            raise ValueError, "itemsize <= 0 for cython.array"

        if not isinstance(format, bytes):
            format = format.encode('ASCII')
        self._format = format  # keep a reference to the byte string
        self.format = self._format

        # use single malloc() for both shape and strides
        self._shape = <isize *>PyObject_Malloc(sizeof(isize)*self.ndim*2)
        self._strides = self._shape + self.ndim

        if not self._shape:
            raise MemoryError, "unable to allocate shape and strides."

        # cdef isize dim, stride
        for idx, dim in enumerate(shape):
            if dim <= 0:
                raise ValueError, f"Invalid shape in axis {idx}: {dim}."
            self._shape[idx] = dim

        let char order
        if mode == 'c':
            order = b'C'
            self.mode = u'c'
        elif mode == 'fortran':
            order = b'F'
            self.mode = u'fortran'
        else:
            raise ValueError, f"Invalid mode, expected 'c' or 'fortran', got {mode}"

        self.len = fill_contig_strides_array(self._shape, self._strides, itemsize, self.ndim, order)

        self.free_data = allocate_buffer
        self.dtype_is_object = format == b'O'

        if allocate_buffer:
            _allocate_buffer(self)

    @cname('getbuffer')
    def __getbuffer__(self, Py_buffer *info, i32 flags):
        let i32 bufmode = -1
        if flags & (PyBUF_C_CONTIGUOUS | PyBUF_F_CONTIGUOUS | PyBUF_ANY_CONTIGUOUS):
            if self.mode == u"c":
                bufmode = PyBUF_C_CONTIGUOUS | PyBUF_ANY_CONTIGUOUS
            elif self.mode == u"fortran":
                bufmode = PyBUF_F_CONTIGUOUS | PyBUF_ANY_CONTIGUOUS
            if not (flags & bufmode):
                raise ValueError, "Can only create a buffer that is contiguous in memory."
        info.buf = self.data
        info.len = self.len

        if flags & PyBUF_STRIDES:
            info.ndim = self.ndim
            info.shape = self._shape
            info.strides = self._strides
        else:
            info.ndim = 1
            info.shape = &self.len if flags & PyBUF_ND else NULL
            info.strides = NULL

        info.suboffsets = NULL
        info.itemsize = self.itemsize
        info.readonly = 0
        info.format = self.format if flags & PyBUF_FORMAT else NULL
        info.obj = self

    def __dealloc__(array self):
        if self.callback_free_data != NULL:
            self.callback_free_data(self.data)
        elif self.free_data and self.data is not NULL:
            if self.dtype_is_object:
                refcount_objects_in_slice(self.data, self._shape, self._strides, self.ndim, inc=False)
            free(self.data)
        PyObject_Free(self._shape)

    @property
    def memview(self):
        return self.get_memview()

    @cname('get_memview')
    cdef get_memview(self):
        flags = PyBUF_ANY_CONTIGUOUS|PyBUF_FORMAT|PyBUF_WRITABLE
        return memoryview(self, flags, self.dtype_is_object)

    def __len__(self):
        return self._shape[0]

    def __getattr__(self, attr):
        return getattr(self.memview, attr)

    def __getitem__(self, item):
        return self.memview[item]

    def __setitem__(self, item, value):
        self.memview[item] = value

    # Sequence methods
    try:
        count = __pyx_collections_abc_Sequence.count
        index = __pyx_collections_abc_Sequence.index
    except:
        pass

@cname("__pyx_array_allocate_buffer")
fn i32 _allocate_buffer(array self) except -1:
    # use malloc() for backwards compatibility
    # in case external code wants to change the data pointer
    let isize i
    let PyObject **p

    self.free_data = True
    self.data = <char *>malloc(self.len)
    if not self.data:
        raise MemoryError, "unable to allocate array data."

    if self.dtype_is_object:
        p = <PyObject **> self.data
        for i in range(self.len // self.itemsize):
            p[i] = Py_None
            Py_INCREF(Py_None)
    return 0

@cname("__pyx_array_new")
fn array array_cwrapper(tuple shape, isize itemsize, char *format, char *c_mode, char *buf):
    let array result
    let str mode = "fortran" if c_mode[0] == b'f' else "c"  # this often comes from a constant C string.

    if buf is NULL:
        result = array.__new__(array, shape, itemsize, format, mode)
    else:
        result = array.__new__(array, shape, itemsize, format, mode, allocate_buffer=False)
        result.data = buf

    return result

#
### Memoryview constants and cython.view.memoryview class
#

# Disable generic_contiguous, as it makes trouble verifying contiguity:
#   - 'contiguous' or '::1' means the dimension is contiguous with dtype
#   - 'indirect_contiguous' means a contiguous list of pointers
#   - dtype contiguous must be contiguous in the first or last dimension
#     from the start, or from the dimension following the last indirect dimension
#
#   e.g.
#           i32[::indirect_contiguous, ::contiguous, :]
#
#   is valid (list of pointers to 2d fortran-contiguous array), but
#
#           i32[::generic_contiguous, ::contiguous, :]
#
#   would mean you'd have assert dimension 0 to be indirect (and pointer contiguous) at runtime.
#   So it doesn't bring any performance benefit, and it's only confusing.

@cname('__pyx_MemviewEnum')
cdef class Enum(object):
    let object name
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

cdef generic = Enum("<strided and direct or indirect>")
cdef strided = Enum("<strided and direct>") # default
cdef indirect = Enum("<strided and indirect>")
# Disable generic_contiguous, as it is a troublemaker
#cdef generic_contiguous = Enum("<contiguous and direct or indirect>")
cdef contiguous = Enum("<contiguous and direct>")
cdef indirect_contiguous = Enum("<contiguous and indirect>")

# 'follow' is implied when the first or last axis is ::1


# pre-allocate thread locks for reuse
## note that this could be implemented in a more beautiful way in "normal" Cython,
## but this code gets merged into the user module and not everything works there.
cdef i32 __pyx_memoryview_thread_locks_used = 0
cdef PyThread_type_lock[{{THREAD_LOCKS_PREALLOCATED}}] __pyx_memoryview_thread_locks = [
{{for _ in range(THREAD_LOCKS_PREALLOCATED)}}
    PyThread_allocate_lock(),
{{endfor}}
]


@cname('__pyx_memoryview')
cdef class memoryview:

    cdef object obj
    cdef object _size
    cdef object _array_interface
    cdef PyThread_type_lock lock
    cdef __pyx_atomic_int_type acquisition_count
    cdef Py_buffer view
    cdef i32 flags
    cdef bint dtype_is_object
    cdef __Pyx_TypeInfo *typeinfo

    def __cinit__(memoryview self, object obj, i32 flags, bint dtype_is_object=False):
        self.obj = obj
        self.flags = flags
        if type(self) is memoryview or obj is not None:
            __Pyx_GetBuffer(obj, &self.view, flags)
            if <PyObject *> self.view.obj == NULL:
                (<__pyx_buffer *> &self.view).obj = Py_None
                Py_INCREF(Py_None)

        if not __PYX_CYTHON_ATOMICS_ENABLED():
            global __pyx_memoryview_thread_locks_used
            if __pyx_memoryview_thread_locks_used < {{THREAD_LOCKS_PREALLOCATED}}:
                self.lock = __pyx_memoryview_thread_locks[__pyx_memoryview_thread_locks_used]
                __pyx_memoryview_thread_locks_used += 1
            if self.lock is NULL:
                self.lock = PyThread_allocate_lock()
                if self.lock is NULL:
                    raise MemoryError

        if flags & PyBUF_FORMAT:
            self.dtype_is_object = (self.view.format[0] == b'O' and self.view.format[1] == b'\0')
        else:
            self.dtype_is_object = dtype_is_object

        assert <Py_intptr_t><void*>(&self.acquisition_count) % sizeof(__pyx_atomic_int_type) == 0
        self.typeinfo = NULL

    def __dealloc__(memoryview self):
        if self.obj is not None:
            __Pyx_ReleaseBuffer(&self.view)
        elif (<__pyx_buffer *> &self.view).obj == Py_None:
            # Undo the incref in __cinit__() above.
            (<__pyx_buffer *> &self.view).obj = NULL
            Py_DECREF(Py_None)

        let i32 i
        global __pyx_memoryview_thread_locks_used
        if self.lock != NULL:
            for i in range(__pyx_memoryview_thread_locks_used):
                if __pyx_memoryview_thread_locks[i] is self.lock:
                    __pyx_memoryview_thread_locks_used -= 1
                    if i != __pyx_memoryview_thread_locks_used:
                        __pyx_memoryview_thread_locks[i], __pyx_memoryview_thread_locks[__pyx_memoryview_thread_locks_used] = (
                            __pyx_memoryview_thread_locks[__pyx_memoryview_thread_locks_used], __pyx_memoryview_thread_locks[i])
                    break
            else:
                PyThread_free_lock(self.lock)

    fn char *get_item_pointer(memoryview self, object index) except NULL:
        let isize dim
        let char *itemp = <char *>self.view.buf

        for dim, idx in enumerate(index):
            itemp = pybuffer_index(&self.view, itemp, idx, dim)

        return itemp

    #@cname('__pyx_memoryview_getitem')
    def __getitem__(memoryview self, object index):
        if index is Ellipsis:
            return self

        have_slices, indices = _unellipsify(index, self.view.ndim)

        let char *itemp
        if have_slices:
            return memview_slice(self, indices)
        else:
            itemp = self.get_item_pointer(indices)
            return self.convert_item_to_object(itemp)

    def __setitem__(memoryview self, object index, object value):
        if self.view.readonly:
            raise TypeError, "Cannot assign to read-only memoryview"

        have_slices, index = _unellipsify(index, self.view.ndim)

        if have_slices:
            obj = self.is_slice(value)
            if obj:
                self.setitem_slice_assignment(self[index], obj)
            else:
                self.setitem_slice_assign_scalar(self[index], value)
        else:
            self.setitem_indexed(index, value)

    fn is_slice(self, obj):
        if not isinstance(obj, memoryview):
            try:
                obj = memoryview(obj, self.flags & ~PyBUF_WRITABLE | PyBUF_ANY_CONTIGUOUS,
                                 self.dtype_is_object)
            except TypeError:
                return None

        return obj

    fn setitem_slice_assignment(self, dst, src):
        let {{memviewslice_name}} dst_slice
        let {{memviewslice_name}} src_slice
        let {{memviewslice_name}} msrc = get_slice_from_memview(src, &src_slice)[0]
        let {{memviewslice_name}} mdst = get_slice_from_memview(dst, &dst_slice)[0]

        memoryview_copy_contents(msrc, mdst, src.ndim, dst.ndim, self.dtype_is_object)

    fn setitem_slice_assign_scalar(self, memoryview dst, value):
        let i32 array[128]
        let void *tmp = NULL
        let void *item

        let {{memviewslice_name}} *dst_slice
        let {{memviewslice_name}} tmp_slice
        dst_slice = get_slice_from_memview(dst, &tmp_slice)

        if <usize>self.view.itemsize > sizeof(array):
            tmp = PyMem_Malloc(self.view.itemsize)
            if tmp == NULL:
                raise MemoryError
            item = tmp
        else:
            item = <void *> array

        try:
            if self.dtype_is_object:
                (<PyObject **> item)[0] = <PyObject *> value
            else:
                self.assign_item_from_object(<char *> item, value)

            # It would be easy to support indirect dimensions, but it's easier
            # to disallow :)
            if self.view.suboffsets != NULL:
                assert_direct_dimensions(self.view.suboffsets, self.view.ndim)
            slice_assign_scalar(dst_slice, dst.view.ndim, self.view.itemsize,
                                item, self.dtype_is_object)
        finally:
            PyMem_Free(tmp)

    fn setitem_indexed(self, index, value):
        let char *itemp = self.get_item_pointer(index)
        self.assign_item_from_object(itemp, value)

    fn convert_item_to_object(self, char *itemp):
        """Only used if instantiated manually by the user, or if Cython doesn't
        know how to convert the type"""
        import r#struct
        let bytes bytesitem
        # Do a manual and complete check here instead of this easy hack
        bytesitem = itemp[:self.view.itemsize]
        try:
            result = r#struct.unpack(self.view.format, bytesitem)
        except r#struct.error:
            raise ValueError, "Unable to convert item to object"
        else:
            if len(self.view.format) == 1:
                return result[0]
            return result

    fn assign_item_from_object(self, char *itemp, object value):
        """Only used if instantiated manually by the user, or if Cython doesn't
        know how to convert the type"""
        import r#struct
        let char c
        let bytes bytesvalue
        let isize i

        if isinstance(value, tuple):
            bytesvalue = r#struct.pack(self.view.format, *value)
        else:
            bytesvalue = r#struct.pack(self.view.format, value)

        for i, c in enumerate(bytesvalue):
            itemp[i] = c

    @cname('getbuffer')
    def __getbuffer__(self, Py_buffer *info, i32 flags):
        if flags & PyBUF_WRITABLE and self.view.readonly:
            raise ValueError, "Cannot create writable memory view from read-only memoryview"

        if flags & PyBUF_ND:
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
        info.readonly = self.view.readonly
        info.obj = self

    # Some properties that have the same semantics as in NumPy
    @property
    def T(self):
        let _memoryviewslice result = memoryview_copy(self)
        transpose_memslice(&result.from_slice)
        return result

    @property
    def base(self):
        return self._get_base()

    fn _get_base(self):
        return self.obj

    @property
    def shape(self):
        return tuple([length for length in self.view.shape[:self.view.ndim]])

    @property
    def strides(self):
        if self.view.strides == NULL:
            # Note: we always ask for strides, so if this is not set it's a bug
            raise ValueError, "Buffer view does not expose strides"

        return tuple([stride for stride in self.view.strides[:self.view.ndim]])

    @property
    def suboffsets(self):
        if self.view.suboffsets == NULL:
            return (-1,) * self.view.ndim

        return tuple([suboffset for suboffset in self.view.suboffsets[:self.view.ndim]])

    @property
    def ndim(self):
        return self.view.ndim

    @property
    def itemsize(self):
        return self.view.itemsize

    @property
    def nbytes(self):
        return self.size * self.view.itemsize

    @property
    def size(self):
        if self._size is None:
            result = 1

            for length in self.view.shape[:self.view.ndim]:
                result *= length

            self._size = result

        return self._size

    def __len__(self):
        if self.view.ndim >= 1:
            return self.view.shape[0]

        return 0

    def __repr__(self):
        return "<MemoryView of %r at 0x%x>" % (self.base.__class__.__name__,
                                               id(self))

    def __str__(self):
        return "<MemoryView of %r object>" % (self.base.__class__.__name__,)

    # Support the same attributes as memoryview slices
    def is_c_contig(self):
        let {{memviewslice_name}} *mslice
        let {{memviewslice_name}} tmp
        mslice = get_slice_from_memview(self, &tmp)
        return slice_is_contig(mslice[0], 'C', self.view.ndim)

    def is_f_contig(self):
        let {{memviewslice_name}} *mslice
        let {{memviewslice_name}} tmp
        mslice = get_slice_from_memview(self, &tmp)
        return slice_is_contig(mslice[0], 'F', self.view.ndim)

    def copy(self):
        let {{memviewslice_name}} mslice
        let i32 flags = self.flags & ~PyBUF_F_CONTIGUOUS

        slice_copy(self, &mslice)
        mslice = slice_copy_contig(&mslice, "c", self.view.ndim,
                                   self.view.itemsize,
                                   flags|PyBUF_C_CONTIGUOUS,
                                   self.dtype_is_object)

        return memoryview_copy_from_slice(self, &mslice)

    def copy_fortran(self):
        let {{memviewslice_name}} src, dst
        let i32 flags = self.flags & ~PyBUF_C_CONTIGUOUS

        slice_copy(self, &src)
        dst = slice_copy_contig(&src, "fortran", self.view.ndim,
                                self.view.itemsize,
                                flags|PyBUF_F_CONTIGUOUS,
                                self.dtype_is_object)

        return memoryview_copy_from_slice(self, &dst)


@cname('__pyx_memoryview_new')
fn memoryview_cwrapper(object o, i32 flags, bint dtype_is_object, __Pyx_TypeInfo *typeinfo):
    let memoryview result = memoryview(o, flags, dtype_is_object)
    result.typeinfo = typeinfo
    return result

@cname('__pyx_memoryview_check')
fn inline bint memoryview_check(object o) noexcept:
    return isinstance(o, memoryview)

fn tuple _unellipsify(object index, i32 ndim):
    """
    Replace all ellipses with full slices and fill incomplete indices with
    full slices.
    """
    let isize idx
    tup = <tuple>index if isinstance(index, tuple) else (index,)

    result = [slice(None)] * ndim
    have_slices = False
    seen_ellipsis = False
    idx = 0
    for item in tup:
        if item is Ellipsis:
            if not seen_ellipsis:
                idx += ndim - len(tup)
                seen_ellipsis = True
            have_slices = True
        else:
            if isinstance(item, slice):
                have_slices = True
            elif not PyIndex_Check(item):
                raise TypeError, f"Cannot index with type '{type(item)}'"
            result[idx] = item
        idx += 1

    nslices = ndim - idx
    return have_slices or nslices, tuple(result)

fn i32 assert_direct_dimensions(isize *suboffsets, i32 ndim) except -1:
    for suboffset in suboffsets[:ndim]:
        if suboffset >= 0:
            raise ValueError, "Indirect dimensions not supported"
    return 0  # return type just used as an error flag

#
### Slicing a memoryview
#

@cname('__pyx_memview_slice')
fn memoryview memview_slice(memoryview memview, object indices):
    let i32 new_ndim = 0, suboffset_dim = -1, dim
    let bint negative_step
    let {{memviewslice_name}} src, dst
    let {{memviewslice_name}} *p_src

    # dst is copied by value in memoryview_fromslice -- initialize it
    # src is never copied
    memset(&dst, 0, sizeof(dst))

    let _memoryviewslice memviewsliceobj

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
    cdef i32 *p_suboffset_dim = &suboffset_dim
    cdef isize start, stop, step, cindex
    cdef bint have_start, have_stop, have_step

    for dim, index in enumerate(indices):
        if PyIndex_Check(index):
            cindex = index
            slice_memviewslice(
                p_dst, p_src.shape[dim], p_src.strides[dim], p_src.suboffsets[dim],
                dim, new_ndim, p_suboffset_dim,
                cindex, 0, 0, # start, stop, step
                0, 0, 0, # have_{start,stop,step}
                False)
        elif index is None:
            p_dst.shape[new_ndim] = 1
            p_dst.strides[new_ndim] = 0
            p_dst.suboffsets[new_ndim] = -1
            new_ndim += 1
        else:
            start = index.start or 0
            stop = index.stop or 0
            step = index.step or 0

            have_start = index.start is not None
            have_stop = index.stop is not None
            have_step = index.step is not None

            slice_memviewslice(
                p_dst, p_src.shape[dim], p_src.strides[dim], p_src.suboffsets[dim],
                dim, new_ndim, p_suboffset_dim,
                start, stop, step,
                have_start, have_stop, have_step,
                True)
            new_ndim += 1

    if isinstance(memview, _memoryviewslice):
        return memoryview_fromslice(dst, new_ndim,
                                    memviewsliceobj.to_object_func,
                                    memviewsliceobj.to_dtype_func,
                                    memview.dtype_is_object)
    else:
        return memoryview_fromslice(dst, new_ndim, NULL, NULL,
                                    memview.dtype_is_object)


#
### Slicing in a single dimension of a memoryviewslice
#

@cname('__pyx_memoryview_slice_memviewslice')
fn i32 slice_memviewslice(
        {{memviewslice_name}} *dst,
        isize shape, isize stride, isize suboffset,
        i32 dim, i32 new_ndim, i32 *suboffset_dim,
        isize start, isize stop, isize step,
        i32 have_start, i32 have_stop, i32 have_step,
        bint is_slice) except -1 nogil:
    """
    Create a new slice dst given slice src.

    dim             - the current src dimension (indexing will make dimensions
                                                 disappear)
    new_dim         - the new dst dimension
    suboffset_dim   - pointer to a single int initialized to -1 to keep track of
                      where slicing offsets should be added
    """

    let isize new_shape
    let bint negative_step

    if not is_slice:
        # index is a normal integer-like index
        if start < 0:
            start += shape
        if not 0 <= start < shape:
            _err_dim(PyExc_IndexError, "Index out of bounds (axis %d)", dim)
    else:
        # index is a slice
        if have_step:
            negative_step = step < 0
            if step == 0:
                _err_dim(PyExc_ValueError, "Step may not be zero (axis %d)", dim)
        else:
            negative_step = False
            step = 1

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

        # len = ceil( (stop - start) / step )
        with cython.cdivision(True):
            new_shape = (stop - start) // step

            if (stop - start) - step * new_shape:
                new_shape += 1

        if new_shape < 0:
            new_shape = 0

        # shape/strides/suboffsets
        dst.strides[new_ndim] = stride * step
        dst.shape[new_ndim] = new_shape
        dst.suboffsets[new_ndim] = suboffset

    # Add the slicing or indexing offsets to the right suboffset or base data *
    if suboffset_dim[0] < 0:
        dst.data += start * stride
    else:
        dst.suboffsets[suboffset_dim[0]] += start * stride

    if suboffset >= 0:
        if not is_slice:
            if new_ndim == 0:
                dst.data = (<char **> dst.data)[0] + suboffset
            else:
                _err_dim(PyExc_IndexError, "All dimensions preceding dimension %d "
                                     "must be indexed and not sliced", dim)
        else:
            suboffset_dim[0] = new_ndim

    return 0

#
### Index a memoryview
#
@cname('__pyx_pybuffer_index')
fn char *pybuffer_index(Py_buffer *view, char *bufp, isize index,
                          isize dim) except NULL:
    let isize shape, stride, suboffset = -1
    let isize itemsize = view.itemsize
    let char *resultp

    if view.ndim == 0:
        shape = view.len // itemsize
        stride = itemsize
    else:
        shape = view.shape[dim]
        stride = view.strides[dim]
        if view.suboffsets != NULL:
            suboffset = view.suboffsets[dim]

    if index < 0:
        index += view.shape[dim]
        if index < 0:
            raise IndexError, f"Out of bounds on buffer access (axis {dim})"

    if index >= shape:
        raise IndexError, f"Out of bounds on buffer access (axis {dim})"

    resultp = bufp + index * stride
    if suboffset >= 0:
        resultp = (<char **> resultp)[0] + suboffset

    return resultp

#
### Transposing a memoryviewslice
#
@cname('__pyx_memslice_transpose')
fn i32 transpose_memslice({{memviewslice_name}} *memslice) except -1 nogil:
    let i32 ndim = memslice.memview.view.ndim

    let isize *shape = memslice.shape
    let isize *strides = memslice.strides

    # reverse strides and shape
    let i32 i, j
    for i in range(ndim // 2):
        j = ndim - 1 - i
        strides[i], strides[j] = strides[j], strides[i]
        shape[i], shape[j] = shape[j], shape[i]

        if memslice.suboffsets[i] >= 0 or memslice.suboffsets[j] >= 0:
            _err(PyExc_ValueError, "Cannot transpose memoryview with indirect dimensions")

    return 0

#
### Creating new memoryview objects from slices and memoryviews
#
@cython.collection_type("sequence")
@cname('__pyx_memoryviewslice')
cdef class _memoryviewslice(memoryview):
    "Internal class for passing memoryview slices to Python"

    # We need this to keep our shape/strides/suboffset pointers valid
    cdef {{memviewslice_name}} from_slice
    # We need this only to print it's class' name
    cdef object from_object

    cdef object (*to_object_func)(char *)
    cdef i32 (*to_dtype_func)(char *, object) except 0

    def __dealloc__(self):
        __PYX_XCLEAR_MEMVIEW(&self.from_slice, 1)

    fn convert_item_to_object(self, char *itemp):
        if self.to_object_func != NULL:
            return self.to_object_func(itemp)
        else:
            return memoryview.convert_item_to_object(self, itemp)

    fn assign_item_from_object(self, char *itemp, object value):
        if self.to_dtype_func != NULL:
            self.to_dtype_func(itemp, value)
        else:
            memoryview.assign_item_from_object(self, itemp, value)

    fn _get_base(self):
        return self.from_object

    # Sequence methods
    try:
        count = __pyx_collections_abc_Sequence.count
        index = __pyx_collections_abc_Sequence.index
    except:
        pass

try:
    if __pyx_collections_abc_Sequence:
        # The main value of registering _memoryviewslice as a
        # Sequence is that it can be used in structural pattern
        # matching in Python 3.10+
        __pyx_collections_abc_Sequence.register(_memoryviewslice)
        __pyx_collections_abc_Sequence.register(array)
except:
    pass  # ignore failure, it's a minor issue

@cname('__pyx_memoryview_fromslice')
fn memoryview_fromslice({{memviewslice_name}} memviewslice,
                          i32 ndim,
                          object (*to_object_func)(char *),
                          i32 (*to_dtype_func)(char *, object) except 0,
                          bint dtype_is_object):

    let _memoryviewslice result

    if <PyObject *>memviewslice.memview == Py_None:
        return None

    # assert 0 < ndim <= memviewslice.memview.view.ndim, (
    #                 ndim, memviewslice.memview.view.ndim)

    result = _memoryviewslice.__new__(_memoryviewslice, None, 0, dtype_is_object)

    result.from_slice = memviewslice
    __PYX_INC_MEMVIEW(&memviewslice, 1)

    result.from_object = (<memoryview> memviewslice.memview)._get_base()
    result.typeinfo = memviewslice.memview.typeinfo

    result.view = memviewslice.memview.view
    result.view.buf = <void *> memviewslice.data
    result.view.ndim = ndim
    (<__pyx_buffer *> &result.view).obj = Py_None
    Py_INCREF(Py_None)

    if (<memoryview>memviewslice.memview).flags & PyBUF_WRITABLE:
        result.flags = PyBUF_RECORDS
    else:
        result.flags = PyBUF_RECORDS_RO

    result.view.shape = <isize *> result.from_slice.shape
    result.view.strides = <isize *> result.from_slice.strides

    # only set suboffsets if actually used, otherwise set to NULL to improve compatibility
    result.view.suboffsets = NULL
    for suboffset in result.from_slice.suboffsets[:ndim]:
        if suboffset >= 0:
            result.view.suboffsets = <isize *> result.from_slice.suboffsets
            break

    result.view.len = result.view.itemsize
    for length in result.view.shape[:ndim]:
        result.view.len *= length

    result.to_object_func = to_object_func
    result.to_dtype_func = to_dtype_func

    return result

@cname('__pyx_memoryview_get_slice_from_memoryview')
fn {{memviewslice_name}} *get_slice_from_memview(memoryview memview,
                                                   {{memviewslice_name}} *mslice) except NULL:
    let _memoryviewslice obj
    if isinstance(memview, _memoryviewslice):
        obj = memview
        return &obj.from_slice
    else:
        slice_copy(memview, mslice)
        return mslice

@cname('__pyx_memoryview_slice_copy')
fn void slice_copy(memoryview memview, {{memviewslice_name}} *dst) noexcept:
    let i32 dim
    let (isize*) shape, strides, suboffsets

    shape = memview.view.shape
    strides = memview.view.strides
    suboffsets = memview.view.suboffsets

    dst.memview = <__pyx_memoryview *> memview
    dst.data = <char *> memview.view.buf

    for dim in range(memview.view.ndim):
        dst.shape[dim] = shape[dim]
        dst.strides[dim] = strides[dim]
        dst.suboffsets[dim] = suboffsets[dim] if suboffsets else -1

@cname('__pyx_memoryview_copy_object')
fn memoryview_copy(memoryview memview):
    "Create a new memoryview object"
    cdef {{memviewslice_name}} memviewslice
    slice_copy(memview, &memviewslice)
    return memoryview_copy_from_slice(memview, &memviewslice)

@cname('__pyx_memoryview_copy_object_from_slice')
fn memoryview_copy_from_slice(memoryview memview, {{memviewslice_name}} *memviewslice):
    """
    Create a new memoryview object from a given memoryview object and slice.
    """
    let object (*to_object_func)(char *)
    let i32 (*to_dtype_func)(char *, object) except 0

    if isinstance(memview, _memoryviewslice):
        to_object_func = (<_memoryviewslice> memview).to_object_func
        to_dtype_func = (<_memoryviewslice> memview).to_dtype_func
    else:
        to_object_func = NULL
        to_dtype_func = NULL

    return memoryview_fromslice(memviewslice[0], memview.view.ndim,
                                to_object_func, to_dtype_func,
                                memview.dtype_is_object)

#
### Copy the contents of a memoryview slices
#
fn isize abs_isize(isize arg) noexcept nogil:
    return -arg if arg < 0 else arg

@cname('__pyx_get_best_slice_order')
fn char get_best_order({{memviewslice_name}} *mslice, i32 ndim) noexcept nogil:
    """
    Figure out the best memory access order for a given slice.
    """
    let i32 i
    let isize c_stride = 0
    let isize f_stride = 0

    for i in range(ndim - 1, -1, -1):
        if mslice.shape[i] > 1:
            c_stride = mslice.strides[i]
            break

    for i in range(ndim):
        if mslice.shape[i] > 1:
            f_stride = mslice.strides[i]
            break

    if abs_isize(c_stride) <= abs_isize(f_stride):
        return 'C'
    else:
        return 'F'

@cython.cdivision(True)
fn void _copy_strided_to_strided(char *src_data, isize *src_strides,
                                   char *dst_data, isize *dst_strides,
                                   isize *src_shape, isize *dst_shape,
                                   i32 ndim, usize itemsize) noexcept nogil:
    # Note: src_extent is 1 if we're broadcasting
    # dst_extent always >= src_extent as we don't do reductions
    let isize i
    let isize src_extent = src_shape[0]
    let isize dst_extent = dst_shape[0]
    let isize src_stride = src_strides[0]
    let isize dst_stride = dst_strides[0]

    if ndim == 1:
        if (src_stride > 0 and dst_stride > 0 and
            <usize> src_stride == itemsize == <usize> dst_stride):
            memcpy(dst_data, src_data, itemsize * dst_extent)
        else:
            for i in range(dst_extent):
                memcpy(dst_data, src_data, itemsize)
                src_data += src_stride
                dst_data += dst_stride
    else:
        for i in range(dst_extent):
            _copy_strided_to_strided(src_data, src_strides + 1,
                                     dst_data, dst_strides + 1,
                                     src_shape + 1, dst_shape + 1,
                                     ndim - 1, itemsize)
            src_data += src_stride
            dst_data += dst_stride

fn void copy_strided_to_strided({{memviewslice_name}} *src,
                                  {{memviewslice_name}} *dst,
                                  i32 ndim, usize itemsize) noexcept nogil:
    _copy_strided_to_strided(src.data, src.strides, dst.data, dst.strides,
                             src.shape, dst.shape, ndim, itemsize)

@cname('__pyx_memoryview_slice_get_size')
fn isize slice_get_size({{memviewslice_name}} *src, i32 ndim) noexcept nogil:
    "Return the size of the memory occupied by the slice in number of bytes"
    let isize shape, size = src.memview.view.itemsize

    for shape in src.shape[:ndim]:
        size *= shape

    return size

@cname('__pyx_fill_contig_strides_array')
fn isize fill_contig_strides_array(
                isize *shape, isize *strides, isize stride,
                i32 ndim, char order) noexcept nogil:
    """
    Fill the strides array for a slice with C or F contiguous strides.
    This is like PyBuffer_FillContiguousStrides, but compatible with py < 2.6
    """
    let i32 idx

    if order == 'F':
        for idx in range(ndim):
            strides[idx] = stride
            stride *= shape[idx]
    else:
        for idx in range(ndim - 1, -1, -1):
            strides[idx] = stride
            stride *= shape[idx]

    return stride

@cname('__pyx_memoryview_copy_data_to_temp')
fn void *copy_data_to_temp({{memviewslice_name}} *src,
                             {{memviewslice_name}} *tmpslice,
                             char order,
                             i32 ndim) except NULL nogil:
    """
    Copy a direct slice to temporary contiguous memory. The caller should free
    the result when done.
    """
    let i32 i
    let void *result

    let usize itemsize = src.memview.view.itemsize
    let usize size = slice_get_size(src, ndim)

    result = malloc(size)
    if not result:
        _err_no_memory()

    # tmpslice[0] = src
    tmpslice.data = <char *> result
    tmpslice.memview = src.memview
    for i in range(ndim):
        tmpslice.shape[i] = src.shape[i]
        tmpslice.suboffsets[i] = -1

    fill_contig_strides_array(&tmpslice.shape[0], &tmpslice.strides[0], itemsize, ndim, order)

    # We need to broadcast strides again
    for i in range(ndim):
        if tmpslice.shape[i] == 1:
            tmpslice.strides[i] = 0

    if slice_is_contig(src[0], order, ndim):
        memcpy(result, src.data, size)
    else:
        copy_strided_to_strided(src, tmpslice, ndim, itemsize)

    return result

# Use 'with gil' functions and avoid 'with gil' blocks, as the code within the blocks
# has temporaries that need the GIL to clean up
@cname('__pyx_memoryview_err_extents')
fn i32 _err_extents(i32 i, isize extent1,
                           isize extent2) except -1 with gil:
    raise ValueError, f"got differing extents in dimension {i} (got {extent1} and {extent2})"

@cname('__pyx_memoryview_err_dim')
fn i32 _err_dim(PyObject *error, str msg, i32 dim) except -1 with gil:
    raise <object>error, msg % dim

@cname('__pyx_memoryview_err')
fn i32 _err(PyObject *error, str msg) except -1 with gil:
    raise <object>error, msg

@cname('__pyx_memoryview_err_no_memory')
fn i32 _err_no_memory() except -1 with gil:
    raise MemoryError


@cname('__pyx_memoryview_copy_contents')
fn i32 memoryview_copy_contents({{memviewslice_name}} src,
                                  {{memviewslice_name}} dst,
                                  i32 src_ndim, i32 dst_ndim,
                                  bint dtype_is_object) except -1 nogil:
    """
    Copy memory from slice src to slice dst.
    Check for overlapping memory and verify the shapes.
    """
    let void *tmpdata = NULL
    let usize itemsize = src.memview.view.itemsize
    let i32 i
    let char order = get_best_order(&src, src_ndim)
    let bint broadcasting = False
    let bint direct_copy = False
    let {{memviewslice_name}} tmp

    if src_ndim < dst_ndim:
        broadcast_leading(&src, src_ndim, dst_ndim)
    elif dst_ndim < src_ndim:
        broadcast_leading(&dst, dst_ndim, src_ndim)

    let i32 ndim = max(src_ndim, dst_ndim)

    for i in range(ndim):
        if src.shape[i] != dst.shape[i]:
            if src.shape[i] == 1:
                broadcasting = True
                src.strides[i] = 0
            else:
                _err_extents(i, dst.shape[i], src.shape[i])

        if src.suboffsets[i] >= 0:
            _err_dim(PyExc_ValueError, "Dimension %d is not direct", i)

    if slices_overlap(&src, &dst, ndim, itemsize):
        # slices overlap, copy to temp, copy temp to dst
        if not slice_is_contig(src, order, ndim):
            order = get_best_order(&dst, ndim)

        tmpdata = copy_data_to_temp(&src, &tmp, order, ndim)
        src = tmp

    if not broadcasting:
        # See if both slices have equal contiguity, in that case perform a
        # direct copy. This only works when we are not broadcasting.
        if slice_is_contig(src, 'C', ndim):
            direct_copy = slice_is_contig(dst, 'C', ndim)
        elif slice_is_contig(src, 'F', ndim):
            direct_copy = slice_is_contig(dst, 'F', ndim)

        if direct_copy:
            # Contiguous slices with same order
            refcount_copying(&dst, dtype_is_object, ndim, inc=False)
            memcpy(dst.data, src.data, slice_get_size(&src, ndim))
            refcount_copying(&dst, dtype_is_object, ndim, inc=True)
            free(tmpdata)
            return 0

    if order == 'F' == get_best_order(&dst, ndim):
        # see if both slices have Fortran order, transpose them to match our
        # C-style indexing order
        transpose_memslice(&src)
        transpose_memslice(&dst)

    refcount_copying(&dst, dtype_is_object, ndim, inc=False)
    copy_strided_to_strided(&src, &dst, ndim, itemsize)
    refcount_copying(&dst, dtype_is_object, ndim, inc=True)

    free(tmpdata)
    return 0

@cname('__pyx_memoryview_broadcast_leading')
fn void broadcast_leading({{memviewslice_name}} *mslice,
                          i32 ndim,
                          i32 ndim_other) noexcept nogil:
    let i32 i
    let i32 offset = ndim_other - ndim

    for i in range(ndim - 1, -1, -1):
        mslice.shape[i + offset] = mslice.shape[i]
        mslice.strides[i + offset] = mslice.strides[i]
        mslice.suboffsets[i + offset] = mslice.suboffsets[i]

    for i in range(offset):
        mslice.shape[i] = 1
        mslice.strides[i] = mslice.strides[0]
        mslice.suboffsets[i] = -1

#
### Take care of refcounting the objects in slices. Do this separately from any copying,
### to minimize acquiring the GIL
#

@cname('__pyx_memoryview_refcount_copying')
fn void refcount_copying({{memviewslice_name}} *dst, bint dtype_is_object, i32 ndim, bint inc) noexcept nogil:
    # incref or decref the objects in the destination slice if the dtype is object
    if dtype_is_object:
        refcount_objects_in_slice_with_gil(dst.data, dst.shape, dst.strides, ndim, inc)

@cname('__pyx_memoryview_refcount_objects_in_slice_with_gil')
fn void refcount_objects_in_slice_with_gil(char *data, isize *shape,
                                           isize *strides, i32 ndim,
                                           bint inc) noexcept with gil:
    refcount_objects_in_slice(data, shape, strides, ndim, inc)

@cname('__pyx_memoryview_refcount_objects_in_slice')
fn void refcount_objects_in_slice(char *data, isize *shape,
                                  isize *strides, i32 ndim, bint inc) noexcept:
    let isize i
    let isize stride = strides[0]

    for i in range(shape[0]):
        if ndim == 1:
            if inc:
                Py_INCREF((<PyObject **> data)[0])
            else:
                Py_DECREF((<PyObject **> data)[0])
        else:
            refcount_objects_in_slice(data, shape + 1, strides + 1, ndim - 1, inc)

        data += stride

#
### Scalar to slice assignment
#
@cname('__pyx_memoryview_slice_assign_scalar')
fn void slice_assign_scalar({{memviewslice_name}} *dst, i32 ndim,
                              usize itemsize, void *item,
                              bint dtype_is_object) noexcept nogil:
    refcount_copying(dst, dtype_is_object, ndim, inc=False)
    _slice_assign_scalar(dst.data, dst.shape, dst.strides, ndim, itemsize, item)
    refcount_copying(dst, dtype_is_object, ndim, inc=True)


@cname('__pyx_memoryview__slice_assign_scalar')
fn void _slice_assign_scalar(char *data, isize *shape,
                             isize *strides, i32 ndim,
                             usize itemsize, void *item) noexcept nogil:
    let isize i
    let isize stride = strides[0]
    let isize extent = shape[0]

    if ndim == 1:
        for i in range(extent):
            memcpy(data, item, itemsize)
            data += stride
    else:
        for i in range(extent):
            _slice_assign_scalar(data, shape + 1, strides + 1, ndim - 1, itemsize, item)
            data += stride


############### BufferFormatFromTypeInfo ###############
extern from *:
    ctypedef struct __Pyx_StructField

    cdef enum:
        __PYX_BUF_FLAGS_PACKED_STRUCT
        __PYX_BUF_FLAGS_INTEGER_COMPLEX

    ctypedef struct __Pyx_TypeInfo:
        char* name
        __Pyx_StructField* fields
        usize size
        usize arraysize[8]
        i32 ndim
        char typegroup
        char is_unsigned
        i32 flags

    ctypedef struct __Pyx_StructField:
        __Pyx_TypeInfo* type
        char* name
        usize offset

    ctypedef struct __Pyx_BufFmt_StackElem:
        __Pyx_StructField* field
        usize parent_offset

    #ctypedef struct __Pyx_BufFmt_Context:
    #  __Pyx_StructField root
        __Pyx_BufFmt_StackElem* head

    struct __pyx_typeinfo_string:
        char string[3]

    __pyx_typeinfo_string __Pyx_TypeInfoToFormat(__Pyx_TypeInfo *)


@cname('__pyx_format_from_typeinfo')
fn bytes format_from_typeinfo(__Pyx_TypeInfo *type):
    let __Pyx_StructField *field
    let __pyx_typeinfo_string fmt
    let bytes part, result
    let isize i

    if type.typegroup == 'S':
        assert type.fields != NULL
        assert type.fields.type != NULL

        if type.flags & __PYX_BUF_FLAGS_PACKED_STRUCT:
            alignment = b'^'
        else:
            alignment = b''

        parts = [b"T{"]
        field = type.fields

        while field.type:
            part = format_from_typeinfo(field.type)
            parts.append(part + b':' + field.name + b':')
            field += 1

        result = alignment.join(parts) + b'}'
    else:
        fmt = __Pyx_TypeInfoToFormat(type)
        result = fmt.string
        if type.arraysize[0]:
            extents = [f"{type.arraysize[i]}" for i in range(type.ndim)]
            result = f"({u','.join(extents)})".encode('ascii') + result

    return result
