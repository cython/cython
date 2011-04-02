# mode: error

cdef signed   float       e
cdef unsigned float       f
cdef signed   double      g
cdef unsigned double      h
cdef signed   long double i
cdef unsigned long double j


_ERRORS = u"""
3:5: Unrecognised type modifier combination
4:5: Unrecognised type modifier combination
5:5: Unrecognised type modifier combination
6:5: Unrecognised type modifier combination
7:5: Unrecognised type modifier combination
8:5: Unrecognised type modifier combination
"""
