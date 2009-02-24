__doc__ = u"""
>>> f0()
(1, 2)
>>> g0()
(1, 2)

>>> f1()
[1, 2]
>>> g1()
[1, 2]

>>> f2()
{1: 2}
>>> g2()
{1: 2}

>>> f3() #doctest: +ELLIPSIS
<argdefault.Foo object at ...>
>>> g3() #doctest: +ELLIPSIS
<argdefault.Foo object at ...>

>>> f4() #doctest: +ELLIPSIS
<argdefault.Bar object at ...>
>>> g4() #doctest: +ELLIPSIS
<argdefault.Bar object at ...>

>>> f5() #doctest: +ELLIPSIS
<argdefault.Bla object at ...>
>>> g5() #doctest: +ELLIPSIS
<argdefault.Bla object at ...>

>>> f6()
7
>>> g6()
7
"""

GLB0 = (1, 2)
def f0(arg=GLB0):
    return arg
def g0(arg=(1, 2)):
    return arg


GLB1 = [1, 2]
def f1(arg=GLB1):
    return arg
def g1(arg=[1, 2]):
    return arg


cdef GLB2 = {1: 2}
def f2(arg=GLB2):
    return arg
def g2(arg={1: 2}):
    return arg


class Foo(object):
    pass
cdef GLB3 = Foo()
def f3(arg=GLB3):
    return arg
def g3(arg=Foo()):
    return arg


cdef class Bar:
    pass
cdef Bar GLB4 = Bar()
def f4(arg=GLB4):
    return arg
def g4(arg=Bar()):
    return arg


cdef class Bla:
    pass
cdef Bla GLB5 = Bla()
def f5(Bla arg=GLB5):
    return arg
def g5(Bla arg=Bla()):
    return arg


cdef int GLB6 = 7
def f6(int arg=GLB6):
    return arg
def g6(int arg=7):
    return arg
