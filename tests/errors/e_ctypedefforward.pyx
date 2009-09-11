ctypedef struct Spam

cdef extern from *:
	ctypedef struct Ham

ctypedef struct Spam:
	int i

ctypedef struct Spam
_ERRORS = u"""
1:0: Forward-referenced type must use 'cdef', not 'ctypedef'
"""
