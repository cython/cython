cimport e_bufaccess_pxd # was needed to provoke a bug involving ErrorType

def f():
    cdef object[e_bufaccess_pxd.T] buf

_ERRORS = u"""
3:9: 'nothing' is not a type identifier
"""
