cdef extern void fa[5]()
cdef extern int af()[5]
cdef extern int ff()()

cdef void f():
	cdef void *p
	cdef int (*h)()
	h = <int ()()>f # this is an error
	h = <int (*)()>f # this is OK
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_declarations.pyx:1:19: Array element cannot be a function
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_declarations.pyx:2:18: Function cannot return an array
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_declarations.pyx:3:18: Function cannot return a function
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_declarations.pyx:8:10: Function cannot return a function
/Local/Projects/D/Pyrex/Source/Tests/Errors3/e_declarations.pyx:8:5: Cannot cast to a function type
"""
