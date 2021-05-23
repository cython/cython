# mode: run
# tag: pure, import, cimport

from cython.cimports.libc import math as libc_math
from cython.cimports.libc.math import ceil as math_ceil

#from cython.cimports cimport libc    # FIXME: currently crashes during analysis when submodule cannot be found
from cython.cimports.libc cimport math
from cython.cimports.libc.math cimport ceil


def libc_math_ceil(x):
    """
    >>> libc_math_ceil(1.5)
    [2, 2, 2, 2]
    """
    return [int(n) for n in [ceil(x), math.ceil(x), libc_math.ceil(x), math_ceil(x)]]
