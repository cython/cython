# ticket: t517
# mode: error

ctypedef void* VoidP

cdef class Spam:
    cdef          VoidP vp0
    cdef readonly VoidP vp2
    cdef public   VoidP vp1

ctypedef struct Foo:
    int i

cdef class Bar:
    cdef          Foo foo0
    cdef readonly Foo foo2
    cdef public   Foo foo1
    pass

_ERRORS = u"""
8:24: C attribute of type 'VoidP' cannot be accessed from Python
8:24: Cannot convert 'VoidP' to Python object
9:24: C attribute of type 'VoidP' cannot be accessed from Python
9:24: Cannot convert 'VoidP' to Python object
9:24: Cannot convert Python object to 'VoidP'
"""

