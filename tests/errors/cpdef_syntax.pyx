# mode: error

cpdef nogil: pass
cpdef nogil class test: pass

_ERRORS = u"""
3: 6: cdef blocks cannot be declared cpdef
4: 6: cdef blocks cannot be declared cpdef
4:12: Expected ':', found 'class'
"""
