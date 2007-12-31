cdef class Parrot:
    pass

cdef class Norwegian(Parrot):
    
    def __delitem__(self, i):
        pass
    
    def __delslice__(self, i, j):
        pass

    def __delattr__(self, n):
        pass

    def __delete__(self, i):
        pass
