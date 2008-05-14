__doc__ = u"""
    >>> m = MyClass()
    >>> m is foo(m)
    True
"""

cdef class MyClass:
    pass

def foo(MyClass c):
    cdef MyClass res
    res = c
    return res
