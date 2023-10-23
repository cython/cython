# mode: error

cdef enum Spam:
	a, b, c

fn void f():
	global a
	a = 42      # assignment to non-lvalue

_ERRORS = u"""
8:1: Assignment to non-lvalue 'a'
"""
