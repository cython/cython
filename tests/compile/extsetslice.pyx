# mode: compile

cdef class Spam:
    def __setslice__(self, isize i, isize j, x):
        pass
