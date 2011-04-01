# mode: compile

cdef class Parrot:
    pass

cdef class Norwegian(Parrot):

    def __setitem__(self, i, x):
        pass

    def __setattr__(self, n, x):
        pass

    def __set__(self, i, v):
        pass
