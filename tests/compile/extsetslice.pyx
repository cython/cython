# mode: compile

cdef class Spam:

    def __setslice__(self, Py_ssize_t i, Py_ssize_t j, x):
        pass
