__doc__ = """
    >>> 
"""

cdef class Eggs:
    cdef object ham

cdef class Spam:
    cdef Eggs eggs

cdef void tomato(Spam s):
    food = s.eggs.ham
