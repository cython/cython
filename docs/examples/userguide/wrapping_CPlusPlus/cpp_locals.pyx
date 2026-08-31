# distutils: language = c++
# cython: cpp_locals = True

from Rectangle cimport Rectangle


cdef class RectOwner:
    cdef Rectangle c_rect  # not initialized

    def __cinit__(self, x, y, w, h):
        self.c_rect = Rectangle(x, y, w, h)  # initialized here

    def getArea(self):
        return self.c_rect.getArea()


def function(dont_write):
    cdef Rectangle c  # not initialized

    if dont_write:
        return c.getArea()  # UnboundLocalError
    else:
        c = Rectangle(1, 2, 3, 4)  # initialized here
        return c.getArea()  # OK
