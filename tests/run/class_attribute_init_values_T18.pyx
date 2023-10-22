# ticket: t18

__doc__ = u"""
>>> f = PyFoo()
>>> print(f.bar)
5
>>> print(f.baz)
someval

>>> f = MyPyFoo()
>>> print(f.bar)
7
>>> print(f.baz)
anotherval

>>> f = CyFoo()
>>> print(f.bar)
5
>>> print(f.baz)
anotherval

>>> f = MyCyFoo()
>>> print(f.bar)
7
>>> print(f.baz)
anotherval

>>> f = AnotherFoo()
>>> print(f.bar)
8
>>> print(f.baz)
yetanotherval
"""

# this works:

class PyFoo(object):
   bar = 5
   baz = u"someval"

class MyPyFoo(PyFoo):
   bar = 7
   baz = u"anotherval"

# this doesn't:

cdef class CyFoo:
    pub i32 bar = 5
    pub object baz = u"someval"

cdef class MyCyFoo(CyFoo):
    pub i32 bar = 7
    pub object baz = u"anotherval"

class AnotherFoo(CyFoo):
    bar = 8
    baz = u"yetanotherval"
