__doc__ = u"""
>>> test(0)
0
>>> test(1)
1
>>> test(2)
2
>>> str(test((1<<32)-1))
'4294967295'

>>> try: test(-1)
... except (OverflowError, TypeError): print("ERROR")
ERROR

>>> test(1<<128) #doctest: +ELLIPSIS
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
>>> try: a.foo(-1)
... except (OverflowError, TypeError): print("ERROR")
ERROR
>>> a.foo(1 << 180) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
"""

# XXX This should generate a warning !!!
cdef extern from *:
    ctypedef unsigned long size_t

def test(size_t i):
    return i

cdef class A:
    cdef public size_t a
    cdef readonly size_t b

    def __init__(self, size_t a, object b):
        self.a = a
        self.b = b

    cpdef size_t foo(self, size_t x):
        cdef object o = x
        return o
