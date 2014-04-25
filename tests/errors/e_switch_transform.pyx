# cython: optimize.use_switch=True
# mode: error

import cython

cdef extern from *:
    enum:
        ONE "1"
        ONE_AGAIN "1+0"

def is_not_one(int i):
    return i != ONE and i != ONE_AGAIN

_FAIL_C_COMPILE = True
