import cython
from cython.cimports.my_module import Shrubbery

@cython.cfunc
def widen_shrubbery(sh: Shrubbery, extra_width):
    sh.width = sh.width + extra_width
