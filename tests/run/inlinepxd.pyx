# mode: run
# tag: inline, pxd

# cython: wraparound = False

__doc__ = u"""
>>> f()
3
>>> g()
6
>>> h()
6
>>> i()
6
>>> j()
6
"""

cimport inlinepxd_support
from inlinepxd_support cimport my_add as my_add3

def f():
    return my_add(1, 2)

def g():
    return inlinepxd_support.my_add(1, 2, 3)

def h():
    return my_add3(1, 2, 3)

def i():
    return my_add3(5)

def j():
    return my_add3(2, 4)

def test_wraparound():
    """
    >>> test_wraparound()
    1.0
    """
    # the wraparound directive from this scope should not affect the inline pxd
    a = [ 0.0, 1.0 ]
    return inlinepxd_support.index(a)


def test_call_inlined(L):
    """
    >>> test_call_inlined([1, 2, 3])
    3
    """
    return inlinepxd_support.call_index(L)
