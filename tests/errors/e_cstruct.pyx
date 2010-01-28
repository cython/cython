cdef struct Spam:
	int i
	char c
	float *p[42]
	obj             # error - py object

#cdef struct Spam: # error - redefined (not an error in Cython, should it be?)
#	int j

cdef struct Grail

cdef void eggs(Spam s):
	cdef int j
	cdef Grail *gp
	j = s.k # error - undef attribute
	j = s.p # type error
	s.p = j # type error
	j = j.i # no error - coercion to Python object
	j.i = j # no error - coercion to Python object
	j = gp.x # error - incomplete type
	gp.x = j # error - incomplete type


_ERRORS = u"""
5:36: C struct/union member cannot be a Python object
15:6: Object of type 'Spam' has no attribute 'k'
16:6: Cannot assign type 'float *[42]' to 'int'
17:21: Cannot assign type 'int' to 'float *[42]'
20:7: Cannot select attribute of incomplete type 'Grail'
21:3: Cannot select attribute of incomplete type 'Grail'
"""
