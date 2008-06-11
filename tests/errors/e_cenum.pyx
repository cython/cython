cdef enum Spam:
	a, b, c

cdef void f():
	global a
	a = 42      # assignment to non-lvalue
	
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_cenum.pyx:6:3: Assignment to non-lvalue 'a'
"""
