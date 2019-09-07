# mode: run
# tag: pure3.9
# cython: language_level=3

# This file tests that methodmangling is applied correctly to
# pure Python decorated classes

import cython

@cython.cclass
class CDefClass:
    """
    #>>> CDefClass.__x
    1
    """
    __x = 1 # Names aren't mangled for cdef classes

class CDefClassInPxd:
    """
    #>>> CDefClassInPxd.__x
    1
    """
    __x = 1 # Names aren't mangled for cdef classes

def declare(**kwargs):
    return kwargs['__x']

class RegularClass:
    @cython.locals(__x=cython.int)
    def f1(self, __x, dummy=None):
        """
        Is the locals decorator correctly applied
        >>> c = RegularClass()
        >>> c.f1(1)
        1
        >>> c.f1("a")
        Traceback (most recent call last):
        ...
        TypeError: an integer is required
        >>> c.f1(_RegularClass__x = 1)
        1
        """
        return __x

    def f2(self, x):
        """
        Is the locals decorator correctly applied
        >>> c = RegularClass()
        >>> c.f2(1)
        1
        >>> c.f2("a")
        Traceback (most recent call last):
        ...
        TypeError: an integer is required
        """
        __x = cython.declare(cython.int, x)

        return __x

    def f3(self, x):
        """
        Is the locals decorator correctly applied
        >>> c = RegularClass()
        >>> c.f3(1)
        1
        >>> c.f3("a")
        Traceback (most recent call last):
        ...
        TypeError: an integer is required
        """
        cython.declare(__x=cython.int)
        __x = x

        return __x

    def f4(self, x):
        """
        We shouldn't be tripped up by a function called
        "declare" that is nothing to do with cython
        >>> RegularClass().f4(1)
        1
        """
        return declare(__x=x)
