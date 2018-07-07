cdef class Shrubbery:
    def __cinit__(self, int w, int l):
        self.width = w
        self.length = l

def standard_shrubbery():
    return Shrubbery(3, 7)
