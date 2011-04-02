# mode: error

cdef spam(int i, char *s = "blarg", float f): # can't have default value
	pass

def swallow(x, y = 42, z): # non-default after default
	pass

cdef class Grail:

	def __add__(x, y = 42): # can't have default value
		pass

_ERRORS = u"""
3:10: Non-default argument follows default argument
3:36: Non-default argument following default argument
6:23: Non-default argument following default argument
11:16: This argument cannot have a default value
"""
