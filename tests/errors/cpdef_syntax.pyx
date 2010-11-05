
cpdef nogil: pass
cpdef nogil class test: pass

_ERRORS = u"""
 2: 6: cdef blocks cannot be declared cpdef
 3: 6: cdef blocks cannot be declared cpdef
 3:12: Expected ':', found 'class'
"""
