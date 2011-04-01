# mode: compile

cdef class Parrot:
    pass

cdef class Norwegian(Parrot):

    def __delitem__(self, i):
        pass

    def __delattr__(self, n):
        pass

    def __delete__(self, i):
        pass
