# mode: error

cdef struct spam:
    pass

ctypedef union eggs:
    pass

enum Ham:
    pass


cdef struct flat_spam: pass

ctypedef union flat_eggs: pass

enum FlatHam: pass


_ERRORS = u"""
3:5: Empty struct or union definition not allowed outside a 'cdef extern from' block
6:0: Empty struct or union definition not allowed outside a 'cdef extern from' block
9:0: Empty enum definition not allowed outside a 'cdef extern from' block

13:5: Empty struct or union definition not allowed outside a 'cdef extern from' block
15:0: Empty struct or union definition not allowed outside a 'cdef extern from' block
17:0: Empty enum definition not allowed outside a 'cdef extern from' block
"""
