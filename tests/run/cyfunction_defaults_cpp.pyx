# cython: binding=True
# mode: run
# tag: cyfunction, cpp

from libcpp.vector cimport vector

cdef class A:
    def f1(self, a, b=1, vector[double] c = vector[double]()):
        pass
    def f2(self, a, b=1,/, vector[double] c = vector[double](1, 2.0)):
        pass
    def f3(self, a, /, b=1, *, c = vector[double](2, 3.0)):
        pass


def check_defaults_on_methods():
    """
    >>> A.f1.__defaults__
    (1, [])
    >>> A.f1.__kwdefaults__
    >>> A.f2.__defaults__
    (1, [2.0])
    >>> A.f2.__kwdefaults__
    >>> A.f3.__defaults__
    (1,)
    >>> A.f3.__kwdefaults__
    {'c': [3.0, 3.0]}
    """
    pass
