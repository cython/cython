# mode: error

cdef pass
cdef void
cdef nogil class test: pass

_ERRORS = u"""
3: 5: Expected an identifier, found 'pass'
4: 9: Empty declarator
5:11: Expected ':', found 'class'
"""
