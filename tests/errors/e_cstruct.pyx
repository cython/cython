# mode: error

cdef struct Spam:
    int i
    char c
    float[42] *p
    obj             # error - py object

#cdef struct Spam: # error - redefined (not an error in Cython, should it be?)
#    int j

cdef struct Grail

cdef void eggs(Spam s):
    cdef int j
    cdef Grail *gp
    j = s.k # error - undef attribute
    j = s.p # type error
    s.p = j # type error
    j = j.i # no error - coercion to Python object
    j.i = j # no error - coercion to Python object
    j = gp.x # error - incomplete type
    gp.x = j # error - incomplete type


_ERRORS = u"""
7:4: C struct/union member cannot be a Python object
17:9: Object of type 'Spam' has no attribute 'k'
18:9: Cannot assign type 'float (*)[42]' to 'int'
19:10: Cannot assign type 'int' to 'float (*)[42]'
22:10: Cannot select attribute of incomplete type 'Grail'
23:6: Cannot select attribute of incomplete type 'Grail'
"""
