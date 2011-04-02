# mode: error

def f():
	cdef char *str1
	cdef float flt1, flt2, flt3
	flt1 = str1 ** flt3 # error
	flt1 = flt2 ** str1 # error

_ERRORS = u"""
6:13: Invalid operand types for '**' (char *; float)
7:13: Invalid operand types for '**' (float; char *)
"""
