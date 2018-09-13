# distutils: language = c++

# matrix.pyx

from libcpp.vector cimport vector

cdef class Matrix:
    cdef unsigned ncols
    cdef vector[float] v

    def __cinit__(self, unsigned ncols):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)
