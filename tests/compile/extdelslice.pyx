# mode: compile

cdef class Spam:

    def __delslice__(self, Py_ssize_t i, Py_ssize_t j):
        pass
