import cython

@cython.cclass
class Shrubbery:
    width = cython.declare(cython.int, visibility='public')
    height = cython.declare(cython.int, visibility='public')
    depth = cython.declare(cython.float, visibility='readonly')
