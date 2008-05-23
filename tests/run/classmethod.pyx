__doc__ = u"""
>>> class1.plus(1)
6
>>> class2.plus(1)
7
>>> class3.plus(1)
8
"""

def f_plus(cls, a):
    return cls.a + a

class class1:
    a = 5
    plus = classmethod(f_plus)

class class2(object):
    a = 6
    plus = classmethod(f_plus)

cdef class class3:
    a = 7
    plus = classmethod(f_plus)
