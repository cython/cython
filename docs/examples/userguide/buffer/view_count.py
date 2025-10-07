# distutils: language = c++

from cython.cimports.cpython import Py_buffer
from cython.cimports.libcpp.vector import vector

@cython.cclass
class Matrix:

    view_count: cython.int

    ncols: cython.Py_ssize_t
    v: vector[cython.float]
    # ...

    def __cinit__(self, ncols: cython.Py_ssize_t):
        self.ncols = ncols
        self.view_count = 0

    def add_row(self):
        if self.view_count > 0:
            raise ValueError("can't add row while being viewed")
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, buffer: cython.pointer[Py_buffer], flags: cython.int):
        # ... as before

        self.view_count += 1

    def __releasebuffer__(self, buffer: cython.pointer[Py_buffer]):
        self.view_count -= 1
