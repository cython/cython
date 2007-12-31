cdef extern from "altet1.h":
    ctypedef int blarg

cdef blarg globvar

def flub(blarg bobble):
    print bobble

globvar = 0
