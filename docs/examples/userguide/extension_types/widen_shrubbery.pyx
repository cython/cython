 
from my_module cimport Shrubbery


cdef widen_shrubbery(Shrubbery sh, extra_width):
    sh.width = sh.width + extra_width
