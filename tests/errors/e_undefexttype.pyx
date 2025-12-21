# mode: error

cdef class Spam
cdef extern class external.Eggs


_ERRORS = u"""
3:0: C class 'Spam' is declared but not defined
4:0: C class 'Eggs' is declared but not defined
"""
