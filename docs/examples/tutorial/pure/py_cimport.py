
from cython.cimports.libc import math

def use_libc_math():
    return math.ceil(5.5)
