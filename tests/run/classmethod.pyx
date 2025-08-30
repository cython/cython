__doc__ = u"""
>>> class1.plus(1)
6
>>> class1.view()
class1
>>> class1().view()
class1
>>> class1.bview()
class1
>>> class1().bview()
class1
>>> class1().cview()
class1
>>> class1().cview("XX")
class1XX

>>> class2.view()
class2
>>> class2.plus(1)
7

>>> class3.view()
class3
>>> class3.bview()
class3
>>> class3().bview()
class3
>>> class3.plus(1)
8

>>> class4.view()
class4
>>> class5.view()
class5
"""

cimport cython

def f_plus(cls, a):
    return cls.a + a

def second_decorator(f):
    # note - a class, not a function (didn't pass Cython's test in __Pyx_Method_ClassMethod)
    class C:
        def __call__(self, *args):
            return f(*args)
    return C()

class class1:
    a = 5
    plus = classmethod(f_plus)
    def view(cls):
        print cls.__name__
    view = classmethod(view)

    @classmethod
    @cython.binding(True)
    def bview(cls):
        print cls.__name__

    @classmethod
    @second_decorator
    def cview(cls, s=""):
        print cls.__name__+s


class class2(object):
    a = 6
    plus = classmethod(f_plus)
    def view(cls):
        print cls.__name__
    view = classmethod(view)


cdef class class3:
    a = 7
    plus = classmethod(f_plus)
    def view(cls):
        print cls.__name__
    view = classmethod(view)

    @classmethod
    @cython.binding(True)
    def bview(cls):
        print cls.__name__


class class4:
    @classmethod
    def view(cls):
        print cls.__name__


class class5(class4):
    pass
