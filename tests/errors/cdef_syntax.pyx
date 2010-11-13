
cdef pass
cdef void
cdef nogil class test: pass

_ERRORS = u"""
 2: 5: Expected an identifier, found 'pass'
 3: 9: Empty declarator
 4:11: Expected ':', found 'class'
"""
