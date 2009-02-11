__doc__ = u"""
>>> test(0)
0
>>> test(1)
1
>>> test(2)
2
>>> str(test((1<<32)-1))
'4294967295'

>>> test(-1) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...

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
>>> a.foo(-1) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
>>> a.foo(1 << 180) #doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
OverflowError: ...
"""

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
