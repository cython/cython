# distutils: language = c++
from cython.cimports.cpython import Py_buffer
from cython.cimports.libcpp.vector import vector

@cython.cclass
class Matrix:
    ncols: cython.Py_ssize_t
    shape: cython.Py_ssize_t[2]
    strides: cython.Py_ssize_t[2]
    v: vector[cython.float]

    def __cinit__(self, ncols: cython.Py_ssize_t):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, buffer: cython.pointer[Py_buffer], flags: cython.int):
        itemsize: cython.Py_ssize_t = cython.sizeof(self.v[0])

        self.shape[0] = self.v.size() // self.ncols
        self.shape[1] = self.ncols

        # Stride 1 is the distance, in bytes, between two items in a row;
        # this is the distance between two adjacent items in the vector.
        # Stride 0 is the distance between the first elements of adjacent rows.
        self.strides[1] = cython.cast(cython.Py_ssize_t, (
             cython.cast(cython.p_char, cython.address(self.v[1]))
           - cython.cast(cython.p_char, cython.address(self.v[0]))
           )
       )
        self.strides[0] = self.ncols * self.strides[1]

        buffer.buf = cython.cast(cython.p_char, cython.address(self.v[0]))
        buffer.format = 'f'                     # float
        buffer.internal = cython.NULL           # see References
        buffer.itemsize = itemsize
        buffer.len = self.v.size() * itemsize   # product(shape) * itemsize
        buffer.ndim = 2
        buffer.obj = self
        buffer.readonly = 0
        buffer.shape = self.shape
        buffer.strides = self.strides
        buffer.suboffsets = cython.NULL         # for pointer arrays only

    def __releasebuffer__(self, buffer: cython.pointer[Py_buffer]):
        pass
