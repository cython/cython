__doc__ = u"""
>>> class1.plus1(1)
2
>>> class2.plus1(1)
2
>>> class3.plus1(1)
2
>>> class4.plus1(1)
2
"""

def f_plus(a):
    return a + 1

class class1:
    plus1 = f_plus

class class2(object):
    plus1 = f_plus

cdef class class3:
    plus1 = f_plus

class class4:
    @staticmethod
    def plus1(a):
        return a + 1
