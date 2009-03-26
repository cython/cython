cdef struct unbekannt
cdef int n
n = sizeof(unbekannt)
_ERRORS = u"""
3:4: Cannot take sizeof incomplete type 'unbekannt'
"""
