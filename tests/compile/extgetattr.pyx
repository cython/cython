# mode: compile

cdef class Spam:

    def __getattr__(self, x):
        pass
