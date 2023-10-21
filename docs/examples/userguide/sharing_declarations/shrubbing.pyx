cdef class Shrubbery:
    def __init__(self, i32 w, i32 l):
        self.width = w
        self.length = l

def standard_shrubbery():
    return Shrubbery(3, 7)
