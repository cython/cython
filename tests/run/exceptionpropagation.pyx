__doc__ = u"""
>>> foo(0)
>>> foo(1)
Traceback (most recent call last):
RuntimeError
"""

cdef int CHKERR(int ierr) except -1:
    if ierr==0: return 0
    raise RuntimeError

cdef int obj2int(object ob) except *:
    return ob

def foo(a):
    cdef int i = obj2int(a)
    CHKERR(i)
