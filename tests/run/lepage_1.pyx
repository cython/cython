cdef class A:
    cdef double x[3]

    def __getitem__(self,i):
        return self.x[i]
