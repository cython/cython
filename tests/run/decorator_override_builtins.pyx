# mode: run
# tag: warnings
# cython: binding=True

from __future__ import print_function

#####
# Tests what happens when the builtin decorators are overridden

def property(func):
    def new_func(*args):
        print("Hello from fake property!", len(args))
    return new_func

def staticmethod(func):
    def new_func(*args):
        print("I'm not really a staticmethod", len(args))
    return new_func

def classmethod(func):
    def new_func(*args):
        print("I'm not really a classmethod", len(args))
    return new_func

def something_else(func):
    def wrapper(*args):
        return func(*args)
    return wrapper

class RegularClass(object):
    """
    Doctests have to be here because if they're in the methods they disappear into oblivion
    >>> RegularClass().prop1()
    Hello from fake property! 1
    >>> RegularClass().prop2()
    Hello from fake property! 1
    >>> RegularClass().sm1()
    I'm not really a staticmethod 1
    >>> RegularClass().sm2()
    I'm not really a staticmethod 1
    >>> RegularClass().sm3()
    I'm not really a staticmethod 1
    >>> RegularClass().cm1()
    I'm not really a classmethod 1
    >>> RegularClass().cm2()
    I'm not really a classmethod 1
    """
    @property
    def prop1(self):
        return "You shouldn't see this"

    @property
    @something_else
    def prop2(self):
        return "You shouldn't see this"

    @staticmethod
    def sm1(self):
        return "You shouldn't see this"

    @staticmethod
    @something_else
    def sm2(self):
        return "You shouldn't see this"

    @something_else
    @staticmethod
    def sm3(self):
        return "You shouldn't see this"

    @classmethod
    def cm1(self):
        return "You shouldn't see this"

    @classmethod
    @something_else
    def cm2(self):
        return "You shouldn't see this"

cdef class CdefClass(object):
    """
    >>> CdefClass().prop1
    "In an ideal world you wouldn't see this, but properties have to be bound early so you will."
    >>> type(CdefClass.prop1).__name__
    'getset_descriptor'

    # TODO eventually should be supported
    # >>> CdefClass().prop2()
    # Hello from fake property! 1
    >>> CdefClass().sm1()
    I'm not really a staticmethod 1
    >>> CdefClass().sm2()
    I'm not really a staticmethod 1
    >>> CdefClass().cm1()
    I'm not really a classmethod 1
    >>> CdefClass().cm2()
    I'm not really a classmethod 1

    """
    @property
    def prop1(self):
        # will get a compile-time warning though
        return "In an ideal world you wouldn't see this, but properties have to be bound early so you will."

    #@property  # TODO eventually should be supported
    #@something_else
    #def prop2(self):
    #    return "You shouldn't see this"

    @staticmethod
    def sm1(self):
        return "You shouldn't see this"

    @staticmethod
    @something_else
    def sm2(self):
        return "You shouldn't see this"

    @classmethod
    def cm1(self):
        return "You shouldn't see this"

    @classmethod
    @something_else
    def cm2(self):
        return "You shouldn't see this"

import sys
if sys.version_info[0] > 2:
    # extra Python3 tests
    """
    >>> RegularClass.prop1()
    Hello from fake property! 0
    >>> RegularClass.prop2()
    Hello from fake property! 0
    >>> RegularClass.sm1()
    I'm not really a staticmethod 0
    >>> RegularClass.sm2()
    I'm not really a staticmethod 0
    >>> RegularClass.sm3()
    I'm not really a staticmethod 0
    >>> RegularClass.cm1()
    I'm not really a classmethod 0
    >>> RegularClass.cm2()
    I'm not really a classmethod 0

    >>> CdefClass.prop2()
    Hello from fake property! 0
    >>> CdefClass.sm1()
    I'm not really a staticmethod 0
    >>> CdefClass.sm2()
    I'm not really a staticmethod 0
    >>> CdefClass.cm1()
    I'm not really a classmethod 0
    >>> CdefClass.cm2()
    I'm not really a classmethod 0
    """
else:
    """
    >>> True
    True
    """

# FIXME I think the "redeclared" warnings are spurious. They certainly aren't what we're interested in testing here
_WARNINGS="""
100:4: Re-assignment of name 'property' was ignored when function was transformed to property of cdef class
114:4: 'sm2' redeclared
114:4: 'sm2' redeclared
116:12: Type of argument 'self' cannot be assumed to be CdefClass because it has an unknown decorator. Consider setting the type explicitly.
123:4: 'cm2' redeclared
123:4: 'cm2' redeclared
125:12: Type of argument 'self' cannot be assumed to be CdefClass because it has an unknown decorator. Consider setting the type explicitly.
"""
