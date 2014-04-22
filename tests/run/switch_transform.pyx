# cython: optimize.switchcase_transform=False

cdef extern from "includes/switch_transform_support.h":
    enum:
        ONE
        ONE_AGAIN

def is_not_one(int i):
    """
    >>> is_not_one(1)
    False
    >>> is_not_one(2)
    True
    """
    return i != ONE and i != ONE_AGAIN
