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
	j = j.i # error - no attributes
	j.i = j # error - no attributes
	j = gp.x # error - incomplete type
	gp.x = j # error - incomplete type
_ERRORS = u"""
5:36: C struct/union member cannot be a Python object
15:6: Object of type 'Spam' has no attribute 'k'
16:6: Cannot assign type 'float *[42]' to 'int'
17:21: Cannot assign type 'int' to 'float *[42]'
18:6: Object of type 'int' has no attribute 'i'
19:2: Object of type 'int' has no attribute 'i'
20:7: Cannot select attribute of incomplete type 'Grail'
21:3: Cannot select attribute of incomplete type 'Grail'
"""
