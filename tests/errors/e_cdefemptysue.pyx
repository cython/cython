cdef struct spam:
	pass

ctypedef union eggs:
	pass

cdef enum ham:
	pass
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_cdefemptysue.pyx:1:5: Empty struct or union definition not allowed outside a 'cdef extern from' block
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_cdefemptysue.pyx:4:0: Empty struct or union definition not allowed outside a 'cdef extern from' block
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_cdefemptysue.pyx:7:5: Empty enum definition not allowed outside a 'cdef extern from' block
"""
