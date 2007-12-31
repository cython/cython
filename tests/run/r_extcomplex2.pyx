__doc__ = """
    >>> c = eggs()
    >>> print "eggs returned:", c
    eggs returned: (17+42j)
    >>> spam(c)
    Real: 17.0
    Imag: 42.0
"""

cdef extern from "complexobject.h":
    
    struct Py_complex:
        double real
        double imag
    
    ctypedef class __builtin__.complex [object PyComplexObject]:
        cdef Py_complex cval
    
def spam(complex c):
    print "Real:", c.cval.real
    print "Imag:", c.cval.imag

def eggs():
    return complex(17, 42)
