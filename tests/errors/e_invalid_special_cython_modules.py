# mode: error
# tag: pure, import, cimport

# nok

import cython.imports.libc as libc_import
import cython.cimports.labc as labc_cimport

from cython.imports import libc
from cython.cimport.libc import math
from cython.imports.libc import math
from cython.cimports.labc import math

import cython.paralel
import cython.parrallel

import cython.dataclass
import cython.floating
import cython.cfunc

# ok
from cython.cimports.libc import math
from cython.cimports.libc.math import ceil


def libc_math_ceil(x):
    """
    >>> libc_math_ceil(1.5)
    [2, 2]
    """
    return [int(n) for n in [ceil(x), math.ceil(x)]]


_ERRORS = """
6:7: 'cython.imports.libc' is not a valid cython.* module. Did you mean 'cython.cimports' ?
7:7: 'labc.pxd' not found
9:0: 'cython.imports' is not a valid cython.* module. Did you mean 'cython.cimports' ?
10:0: 'cython.cimport.libc' is not a valid cython.* module. Did you mean 'cython.cimports' ?
11:0: 'cython.imports.libc' is not a valid cython.* module. Did you mean 'cython.cimports' ?
12:0: 'labc/math.pxd' not found
14:7: 'cython.paralel' is not a valid cython.* module. Did you mean 'cython.parallel' ?
15:7: 'cython.parrallel' is not a valid cython.* module. Did you mean 'cython.parallel' ?
17:7: 'cython.dataclass' is not a valid cython.* module. Did you mean 'cython.dataclasses' ?
18:7: 'cython.floating' is not a valid cython.* module. Instead, use 'import cython' and then 'cython.floating'.
19:7: 'cython.cfunc' is not a valid cython.* module. Instead, use 'import cython' and then 'cython.cfunc'.
"""
