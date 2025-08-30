# -*- coding: utf-8 -*-
# mode: run
# tag: pep3131, traceback

# cython: language_level=3

# Code with unicode identifiers can be compiled with Cython running either Python 2 or 3.
# However Python access to unicode identifiers is only possible in Python 3. In Python 2
# it's only really safe to use the unicode identifiers for purely Cython interfaces
# (although this isn't enforced...). Therefore the majority of the doctests are
# Python3 only and only a limited set are run in Python2.
# This is controlled by putting the Python3 only tests in the module __doc__ attribute
# Most of the individual function and class docstrings are only present as a compile test

cimport cython

import sys


__doc__ = u"""
    >>> f()()
    2
    >>> f().__name__
    'nεsted'

    The test is mainly to see if the traceback is generated correctly
    >>> print_traceback_name()
    unicode_identifiers.Fα1

    Just check that a cpdef function is callable
    >>> Fα3()
    1

    >>> Γναμε2.ναμε3
    1
    >>> x = Γναμε2()
    >>> print(x.α)
    100
    >>> x.α = 200
    >>> print(x.α)
    200

    >>> B().Ƒ()
    >>> C().Ƒ()

    Test generation of locals()
    >>> sorted(Γναμε2().boring_function(1,2).keys())
    ['self', 'somevalue', 'x', 'ναμε5', 'ναμε6']

    >>> Γναμε2().boring_cpdef() - Γναμε2().εxciting_cpdef()
    0
    >>> function_taking_fancy_argument(Γναμε2()).ναμε3
    1
    >>> metho_function_taking_fancy_argument(Γναμε2()).ναμε3
    1
    >>> NormalClassΓΓ().ναμε
    10
    >>> NormalClassΓΓ().εxciting_function(None).__qualname__
    'NormalClassΓΓ.εxciting_function.<locals>.nestεd'

    Do kwargs work?
    >>> unicode_kwarg(αrγ=5)
    5
    >>> unicode_kwarg_from_cy()
    1

    Normalization of attributes
    (The cdef class version is testable in Python 2 too)
    >>> NormalizeAttrPy().get()
    5
    """

global_ναμε1 = None
cdef double global_ναμε2 = 1.2

def f():
    """docstring"""
    ναμε2 = 2
    def nεsted():
        return ναμε2
    return nεsted

# Ƒ is notably awkward because its punycode starts with "2" causing
# C compile errors. Therefore try a few different variations...
cdef class A:
    cdef int ναμε
    def __init__(self):
        self.ναμε = 1
    cdef Ƒ(self):
        return self.ναμε == 1
    def regular_function(self):
        """
        Can use unicode cdef functions and (private) attributes internally
        >>> A().regular_function()
        True
        """
        return self.Ƒ()
cdef class B:
    cpdef Ƒ(self):
        pass
cdef class C:
    def Ƒ(self):
        pass
cdef class D:
    cdef int Ƒ

def regular_function():
    """
    Unicode names can be used internally on python2
    >>> regular_function()
    10
    """
    cdef int variableƑ = 5
    ναμε2 = 2
    return variableƑ*ναμε2

cdef Fα1():
    """docstring"""
    ναμε2 = 2
    raise RuntimeError() # forces generation of a traceback

def print_traceback_name():
    try:
        Fα1()
    except RuntimeError as e:
        import traceback
        # get the name of one level up in the traceback
        print(traceback.extract_tb(e.__traceback__,2)[1][2])


def Fα2():
    """docstring"""
    def nested_normal():
        """docstring"""
        pass
    def nεstεd_uni():
        """docstring"""
        pass
    return nested_normal, nεstεd_uni

cpdef Fα3():
    """docstring"""
    return 1

cdef class Γναμε2:
    """
    docstring
    """
    ναμε3 = 1

    def __init__(self):
        self.α = 100
    def boring_function(self,x,ναμε5):
        """docstring"""
        ναμε6 = ναμε5
        somevalue = global_ναμε1 == self.ναμε3
        return locals()
    def εxciting_function(self,y):
        """docstring"""
        def nestεd():
            pass
        return nestεd

    cdef boring_cdef(self):
        """docstring"""
        pass
    cdef εxciting_cdef(self):
        """docstring"""
        pass

    cpdef boring_cpdef(self):
        """docstring"""
        return 2
    cpdef εxciting_cpdef(self):
        """docstring"""
        return 2
    cpdef cpdef_with_exciting_arg(self, ααα):
        """
        >>> Γναμε2().cpdef_with_exciting_arg(5)
        5
        """
        return ααα

cdef class Derived(Γναμε2):
    pass

cdef Γναμε2 global_ναμε3 = Γναμε2()


@cython.always_allow_keywords(False)  # METH_O signature
def metho_function_taking_fancy_argument(Γναμε2 αrγ):
    return αrγ

@cython.always_allow_keywords(True)
def function_taking_fancy_argument(Γναμε2 αrγ):
    return αrγ


class NormalClassΓΓ(Γναμε2):
    """
    docstring
    """
    def __init__(self):
        self.ναμε = 10

    def boring_function(self,x,ναμε5):
        """docstring"""
        ναμε6 = ναμε5
        somevalue = global_ναμε1 == self.ναμε3
        return locals()
    def εxciting_function(self,y):
        """docstring"""
        def nestεd():
            pass
        return nestεd

def unicode_kwarg(*, αrγ):
    return αrγ

def unicode_kwarg_from_cy():
    return unicode_kwarg(αrγ=1)

class NormalizeAttrPy:
    """Python normalizes identifier names before they are used;
    therefore ﬁ and fi should access the same attribute"""
    def __init__(self):
        self.ﬁ = 5 # note unicode ligature symbol
    def get(self):
        return self.fi

cdef class NormalizeAttrCdef:
    """Python normalizes identifier names before they are used;
    therefore ﬁ and fi should access the same attribute
    >>> NormalizeAttrCdef().get()
    5
    """
    cdef int ﬁ # note unicode ligature symbol
    def __init__(self):
        self.fi = 5
    def get(self):
        return self.ﬁ


ctypedef long äntägär

def use_typedef(x: äntägär):
    """
    >>> use_typedef(5)
    10
    """
    cdef äntägär i = x
    return i + x


ctypedef fused nümbärs:
    float
    äntägär


def use_fused_typedef(x: nümbärs):
    """
    >>> use_fused_typedef(4)
    8
    >>> use_fused_typedef(4.5)
    9.0
    """
    cdef nümbärs i = x
    assert cython.typeof(i) in ('float', 'äntägär'), cython.typeof(i)
    return i + x
