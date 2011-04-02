# mode: error

ctypedef struct Spam

cdef extern from *:
	ctypedef struct Ham

ctypedef struct Spam:
	int i

ctypedef struct Spam
_ERRORS = u"""
3:0: Forward-referenced type must use 'cdef', not 'ctypedef'
"""
