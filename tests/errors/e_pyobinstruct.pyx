cdef object x

cdef struct spam:
	object parrot

def f():
	cdef spam s
	s.parrot = x
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_pyobinstruct.pyx:4:8: C struct/union member cannot be a Python object
"""
