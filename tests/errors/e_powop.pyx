def f():
	cdef char *str1
	cdef float flt1, flt2, flt3
	cdef int int1 = 1, int2 = 2, int3
	flt1 = str1 ** flt3 # error
	flt1 = flt2 ** str1 # error
	int3 = int1 ** int2 # disabled in Cython
	int3 = 3 ** 4       # disabled in Cython

_ERRORS = u"""
5:13: Invalid operand types for '**' (char *; float)
6:13: Invalid operand types for '**' (float; char *)
7:13: C has no integer powering, use python ints or floats instead '**' (int; int)
8:10: C has no integer powering, use python ints or floats instead '**' (long; long)
"""
