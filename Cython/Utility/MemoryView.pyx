########## CythonArray ##########

cdef extern from "stdlib.h":
    void *malloc(size_t)
    void free(void *)

cdef extern from "Python.h":

    cdef enum:
        PyBUF_C_CONTIGUOUS,
        PyBUF_F_CONTIGUOUS,
        PyBUF_ANY_CONTIGUOUS


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
        info.format = self.format
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

@cname("__pyx_array_new")
cdef array array_cwrapper(tuple shape, Py_ssize_t itemsize, char *format, char *mode):
    return array(shape, itemsize, format, mode.decode('ASCII'))

########## MemoryView ##########

# from cpython cimport ...
cdef extern from "pythread.h":

    ctypedef void *PyThread_type_lock

    PyThread_type_lock PyThread_allocate_lock()
    void PyThread_free_lock(PyThread_type_lock)
    int PyThread_acquire_lock(PyThread_type_lock, int mode) nogil
    void PyThread_release_lock(PyThread_type_lock) nogil

cdef extern from *:
    int __Pyx_GetBuffer(object, Py_buffer *, int)
    void __Pyx_ReleaseBuffer(Py_buffer *)


@cname('__pyx_MemviewEnum')
cdef class Enum(object):
    cdef object name
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name


cdef strided = Enum("<strided axis packing mode>")
cdef contig = Enum("<contig axis packing mode>")
cdef follow = Enum("<follow axis packing mode>")
cdef direct = Enum("<direct axis access mode>")
cdef ptr = Enum("<ptr axis access mode>")
cdef full = Enum("<full axis access mode>")


@cname('__pyx_memoryview')
cdef class memoryview(object):

    cdef object obj
    cdef Py_buffer view
    cdef PyThread_type_lock acqcnt_lock
    cdef int acquisition_count

    def __cinit__(memoryview self, object obj, int flags):
        self.obj = obj
        #self.acqcnt_lock = PyThread_allocate_lock()
        #if self.acqcnt_lock == NULL:
        #    raise MemoryError

        __Pyx_GetBuffer(obj, &self.view, flags)

    def __dealloc__(memoryview self):
        #PyThread_free_lock(self.acqcnt_lock)
        self.obj = None
        __Pyx_ReleaseBuffer(&self.view)


@cname('__pyx_memoryview_new')
cdef memoryview memoryview_cwrapper(object o, int flags):
    return memoryview(o, flags)
