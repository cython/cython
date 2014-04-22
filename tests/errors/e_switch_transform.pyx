# cython: optimize.switchcase_transform=True
# mode: error

import cython

cdef extern from "includes/e_switch_transform_support.h":
    enum:
        ONE
        ONE_AGAIN

def is_not_one(int i):
    return i != ONE and i != ONE_AGAIN

_ERRORS = u'''
runtime error
'''
