# mode: error

cdef enum Spam:
	a, b, c

cdef void f():
	global a
	a = 42      # assignment to non-lvalue

_ERRORS = u"""
8:3: Assignment to non-lvalue 'a'
"""
