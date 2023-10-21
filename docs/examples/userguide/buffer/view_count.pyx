# distutils: language = c++

from cpython cimport Py_buffer
from libcpp.vector cimport vector

cdef class Matrix:
    cdef i32 view_count
    cdef isize ncols
    cdef vector[f32] v
    # ...

    def __cinit__(self, isize ncols):
        self.ncols = ncols
        self.view_count = 0

    def add_row(self):
        if self.view_count > 0:
            raise ValueError("can't add row while being viewed")
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, Py_buffer *buffer, i32 flags):
        # ... as before

        self.view_count += 1

    def __releasebuffer__(self, Py_buffer *buffer):
        self.view_count -= 1
