# mode: run
# ticket: t494
# cython: binding=True


class A:
    """
    >>> A.foo = foo
    >>> A().foo()
    True
    """
    pass

def foo(self):
    return self is not None


cimport cython

# with binding==False assignment of functions always worked - doesn't match Python
# behaviour but ensures Cython behaviour stays consistent

def f_plus(a):
    return a + 1

@cython.binding(False)
def f_plus_nobind(a):
    return a+1

cdef class B:
    """
    >>> B.plus1(1)
    2
    >>> B.plus1_nobind(1)
    2
    """
    plus1 = f_plus
    plus1_nobind = f_plus_nobind


