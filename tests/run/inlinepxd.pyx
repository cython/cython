__doc__ = u"""
>>> f()
3
>>> g()
6
>>> h()
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
