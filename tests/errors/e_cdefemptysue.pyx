cdef struct spam:
	pass

ctypedef union eggs:
	pass

cdef enum ham:
	pass
_ERRORS = u"""
1:5: Empty struct or union definition not allowed outside a 'cdef extern from' block
4:0: Empty struct or union definition not allowed outside a 'cdef extern from' block
7:5: Empty enum definition not allowed outside a 'cdef extern from' block
"""
