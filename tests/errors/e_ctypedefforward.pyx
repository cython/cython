ctypedef struct Spam
ctypedef class Eggs

cdef extern from *:
	ctypedef struct Ham

ctypedef struct Spam:
	int i

ctypedef class Eggs:
	pass

ctypedef struct Spam
ctypedef class Eggs
_ERRORS = u"""
1:0: Forward-referenced type must use 'cdef', not 'ctypedef'
2:0: Forward-referenced type must use 'cdef', not 'ctypedef'
"""
