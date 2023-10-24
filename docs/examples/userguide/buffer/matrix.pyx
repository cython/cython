# distutils: language = c++

from libcpp.vector cimport vector

cdef class Matrix:
    cdef u32 ncols
    cdef vector[f32] v

    def __cinit__(self, u32 ncols):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)
