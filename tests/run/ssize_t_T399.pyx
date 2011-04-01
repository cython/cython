# ticket: 399

__doc__ = u"""
>>> test(-2)
-2
>>> test(-1)
-1
>>> test(0)
0
>>> test(1)
1
>>> test(2)
2

>>> test(SSIZE_T_MAX) == SSIZE_T_MAX
True
>>> test(SSIZE_T_MIN) == SSIZE_T_MIN
True

>>> test(SSIZE_T_MAX+1) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
>>> test(SSIZE_T_MIN-1) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...

>>> test(1<<128) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
>>> test(-(1<<128)) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...

>>> a = A(1,2)
>>> a.a == 1
True
>>> a.b == 2
True
>>> a.foo(5)
5
>>> a.foo(1 << 180) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
"""

cdef extern from *:
    ctypedef long ssize_t # XXX This should generate a warning !!!
    ssize_t PY_SSIZE_T_MAX
    ssize_t PY_SSIZE_T_MIN

SSIZE_T_MAX = PY_SSIZE_T_MAX
SSIZE_T_MIN = PY_SSIZE_T_MIN

def test(ssize_t i):
    return i

cdef class A:
    cdef public ssize_t a
    cdef readonly ssize_t b

    def __init__(self, ssize_t a, object b):
        self.a = a
        self.b = b

    cpdef ssize_t foo(self, ssize_t x):
        cdef object o = x
        return o
