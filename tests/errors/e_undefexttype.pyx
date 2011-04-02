# mode: error

cdef class Spam
cdef extern class external.Eggs
_ERRORS = u"""
3:5: C class 'Spam' is declared but not defined
4:5: C class 'Eggs' is declared but not defined
"""
