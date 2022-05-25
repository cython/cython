# mode: error

cdef struct spam:
	pass

ctypedef union eggs:
	pass

cdef enum ham:
	pass


cdef struct flat_spam: pass

ctypedef union flat_eggs: pass

cdef enum flat_ham: pass


_ERRORS = u"""
3:5: Empty struct or union definition not allowed outside a 'cdef extern from' block
6:0: Empty struct or union definition not allowed outside a 'cdef extern from' block
9:5: Empty enum definition not allowed outside a 'cdef extern from' block

13:5: Empty struct or union definition not allowed outside a 'cdef extern from' block
15:0: Empty struct or union definition not allowed outside a 'cdef extern from' block
17:5: Empty enum definition not allowed outside a 'cdef extern from' block
"""
