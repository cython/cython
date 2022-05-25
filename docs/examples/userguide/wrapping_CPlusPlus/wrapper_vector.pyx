# distutils: language = c++

from libcpp.vector cimport vector


cdef class VectorStack:
    cdef vector[int] v

    def push(self, x):
        self.v.push_back(x)

    def pop(self):
        if self.v.empty():
            raise IndexError()
        x = self.v.back()
        self.v.pop_back()
        return x
