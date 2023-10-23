# cython: optimize.use_switch=true
# mode: error
# tag: cerror

import cython

extern from *:
    enum:
        ONE "1"
        ONE_AGAIN "1+0"

def is_not_one(i32 i):
    return i != ONE and i != ONE_AGAIN
