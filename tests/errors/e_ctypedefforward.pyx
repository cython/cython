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
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_ctypedefforward.pyx:1:0: Forward-referenced type must use 'cdef', not 'ctypedef'
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_ctypedefforward.pyx:2:0: Forward-referenced type must use 'cdef', not 'ctypedef'
"""
