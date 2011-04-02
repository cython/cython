# mode: error

cdef struct unbekannt
cdef int n
n = sizeof(unbekannt)
_ERRORS = u"""
5:4: Cannot take sizeof incomplete type 'unbekannt'
"""
