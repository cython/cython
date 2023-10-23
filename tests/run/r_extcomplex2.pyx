__doc__ = u"""
    >>> c = eggs()
    >>> c
    (17+42j)
    >>> spam(c)
    Real: 17.0
    Imag: 42.0
"""

extern from "complexobject.h":
    struct Py_complex:
        f64 real
        f64 imag

    ctypedef class __builtin__.complex [object PyComplexObject]:
        cdef Py_complex cval

def spam(complex c):
    print u"Real:", c.cval.real
    print u"Imag:", c.cval.imag

def eggs():
    return complex(17, 42)
