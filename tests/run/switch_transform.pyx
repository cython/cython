# cython: optimize.use_switch=False
# cython: linetrace=True

cdef extern from *:
    enum:
        ONE "1"
        ONE_AGAIN "1+0"

def is_not_one(int i):
    """
    >>> is_not_one(1)
    False
    >>> is_not_one(2)
    True
    """
    return i != ONE and i != ONE_AGAIN
