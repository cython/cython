cdef struct unbekannt
cdef int n
n = sizeof(unbekannt)
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_sizeofincomplete.pyx:3:4: Cannot take sizeof incomplete type 'unbekannt'
"""
