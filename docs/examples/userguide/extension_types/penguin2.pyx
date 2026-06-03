cimport cython


@cython.freelist(8)
cdef class Penguin:
    cdef object food
    def __cinit__(self, food):
        self.food = food

penguin = Penguin('fish 1')
penguin = None
penguin = Penguin('fish 2')  # does not need to allocate memory!
