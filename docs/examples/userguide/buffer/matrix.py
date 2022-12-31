# distutils: language = c++

from cython.cimports.libcpp.vector import vector

@cython.cclass
class Matrix:
    ncols: cython.unsigned
    v: vector[cython.float]

    def __cinit__(self, ncols: cython.unsigned):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)
