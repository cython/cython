# mode: compile

cdef class Spam:
    def __delslice__(self, isize i, isize j):
        pass
