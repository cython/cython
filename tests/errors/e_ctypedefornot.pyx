cdef struct Foo

ctypedef struct Foo:
	int i
	
ctypedef struct Blarg:
	char c

cdef struct Blarg

cdef class Spam

ctypedef class Spam:
	pass
	
cdef Foo f
cdef Blarg b

_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_ctypedefornot.pyx:3:0: 'Foo' previously declared using 'cdef'
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_ctypedefornot.pyx:9:5: 'Blarg' previously declared using 'ctypedef'
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_ctypedefornot.pyx:13:0: 'Spam' previously declared using 'cdef'
"""
