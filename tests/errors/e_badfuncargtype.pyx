cdef struct Spam

cdef extern int spam(void)           # function argument cannot be void
cdef extern int grail(int i, void v) # function argument cannot be void
cdef int tomato(Spam s):             # incomplete type
	pass

_ERRORS = u"""
3:21: Use spam() rather than spam(void) to declare a function with no arguments.
4:29: Use spam() rather than spam(void) to declare a function with no arguments.
5:16: Argument type 'Spam' is incomplete
"""
