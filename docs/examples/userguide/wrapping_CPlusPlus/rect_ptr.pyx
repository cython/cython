# distutils: language = c++

from Rectangle cimport Rectangle

cdef class PyRectangle:
    cdef Rectangle*c_rect  # hold a pointer to the C++ instance which we're wrapping

    def __cinit__(self):
        self.c_rect = new Rectangle()

    def __init__(self, int x0, int y0, int x1, int y1):
        if self.c_rect:
            del self.c_rect
        self.c_rect = new Rectangle(x0, y0, x1, y1)

    def __dealloc__(self):
        del self.c_rect
