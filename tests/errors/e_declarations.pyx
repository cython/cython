# mode: error

cdef extern void fa[5]()
cdef extern int af()[5]
cdef extern int ff()()

cdef void f():
	cdef void *p
	cdef int (*h)()
	h = <int ()()>f # this is an error
	h = <int (*)()>f # this is OK


_ERRORS = u"""
3:19: Array element cannot be a function
5:18: Function cannot return a function
10:10: Function cannot return a function
10:5: Cannot cast to a function type
"""
