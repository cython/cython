# cython: optimize.use_switch=True
# mode: error
# tag: cerror

import cython

cdef extern from *:
    enum:
        ONE "1"
        ONE_AGAIN "1+0"

def is_not_one(int i):
    return i != ONE and i != ONE_AGAIN
