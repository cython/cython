# mode: compile

cdef class Spam:

    def __delattr__(self, n):
        pass
