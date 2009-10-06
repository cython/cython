cdef spam(int i, char *s = "blarg", float f): # can't have default value
	pass

def swallow(x, y = 42, z): # non-default after default
	pass

cdef class Grail:

	def __add__(x, y = 42): # can't have default value
		pass

_ERRORS = u"""
1:10: Non-default argument follows default argument
1:36: Non-default argument following default argument
4:23: Non-default argument following default argument
9:16: This argument cannot have a default value
"""
