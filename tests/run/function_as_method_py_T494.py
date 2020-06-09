# ticket: 494

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
    __doc__ = u"""
>>> B.plus1(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TypeError: unbound
>>> C.plus1(1) #doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
TypeError: unbound
"""
else:
    __doc__ = u"""
>>> B.plus1(1)
2
>>> C.plus1(1)
2
"""

def f_plus(a):
    return a + 1

class B:
    plus1 = f_plus

class C(object):
    plus1 = f_plus
