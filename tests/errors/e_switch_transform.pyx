# cython: optimize.use_switch=True
# mode: error

import cython

cdef extern from "../run/includes/switch_transform_support.h":
    enum:
        ONE
        ONE_AGAIN

def is_not_one(int i):
    return i != ONE and i != ONE_AGAIN

_ERRORS = u'''
runtime error
'''
