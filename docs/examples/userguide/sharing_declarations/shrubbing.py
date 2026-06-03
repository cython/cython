import cython

@cython.cclass
class Shrubbery:
    def __cinit__(self, w: cython.int, l: cython.int):
        self.width = w
        self.length = l

def standard_shrubbery():
    return Shrubbery(3, 7)
