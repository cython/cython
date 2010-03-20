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
5:24: C attribute of type 'VoidP' cannot be accessed from Python
5:24: Cannot convert 'VoidP' to Python object
6:24: C attribute of type 'VoidP' cannot be accessed from Python
6:24: Cannot convert 'VoidP' to Python object
6:24: Cannot convert Python object to 'VoidP'
14:22: C attribute of type 'Foo' cannot be accessed from Python
14:22: Cannot convert Python object to 'Foo'
"""

