__doc__ = """
    >>> flub(25)
    25
    >>> g()
    0
"""

cdef extern from "altet1.h":
    ctypedef int blarg

cdef blarg globvar

def flub(blarg bobble):
    print bobble

globvar = 0

def g():
    return globvar
