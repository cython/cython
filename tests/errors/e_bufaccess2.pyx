cimport e_bufaccess_pxd # was needed to provoke a bug involving ErrorType

def f():
    cdef object[e_bufaccess_pxd.T] buf

_ERRORS = u"""
3:17: Syntax error in ctypedef statement
4:31: 'T' is not a type identifier
4:31: 'T' is not declared
"""
