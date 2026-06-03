import cython
from cython.cimports.my_module import Shrubbery

@cython.cfunc
def another_shrubbery(sh1: Shrubbery) -> Shrubbery:
    sh2: Shrubbery
    sh2 = Shrubbery()
    sh2.width = sh1.width
    sh2.height = sh1.height
    return sh2
