# ticket: 494
# cython: binding=True

__doc__ = """
    >>> A.foo = foo
    >>> A().foo()
    True
"""

class A:
    pass

def foo(self):
    return self is not None

# assignment of functions used in a "static method" type way behaves differently
# in Python2 and 3
import sys
if sys.version_info[0] == 2:
    __doc__ = """>>> B.plus1(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TypeError: unbound
"""
else:
    __doc__ = """>>> B.plus1(1)
2
"""

# with binding==False assignment of functions always worked - doesn't match Python
# behaviour but ensures Cython behaviour stays consistent
__doc__ += """
>>> B.plus1_nobind(1)
2
"""

cimport cython

def f_plus(a):
    return a + 1

@cython.binding(False)
def f_plus_nobind(a):
    return a+1

cdef class B:
    plus1 = f_plus
    plus1_nobind = f_plus_nobind


