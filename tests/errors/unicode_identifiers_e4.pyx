# -*- coding: utf-8 -*-
# mode: error

cdef class C:
    # these two symbols "\u1e69" and "\u1e9b\u0323" normalize to the same thing
    # so the two attributes can't coexist
    cdef int ṩomething
    cdef double ẛ̣omething

_ERRORS = u"""
7:13: Previous declaration is here
8:16: 'ṩomething' redeclared
"""
