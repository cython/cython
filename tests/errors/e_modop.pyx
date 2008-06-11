def f():
	cdef float flt1, flt2, flt3
	flt1 = flt2 % flt3 # error
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_modop.pyx:3:13: Invalid operand types for '%' (float; float)
"""
