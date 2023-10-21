# -*- coding: utf-8 -*-
# mode: error

cdef class C:
    # these two symbols "\u1e69" and "\u1e9b\u0323" normalize to the same thing
    # so the two attributes can't coexist
    cdef i32 ṩomething
    cdef f64 ẛ̣omething

_ERRORS = u"""
7:13: Previous declaration is here
8:13: 'ṩomething' redeclared
"""
