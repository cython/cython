# ticket: t373

import math

cdef class MyClass:
    """
    >>> x=MyClass()
    4
    """
    def __cinit__(self, int arg=2*2):
        print arg

cdef class MyOtherClass:
    """
    >>> x=MyOtherClass()
    8
    """
    def __cinit__(self, int arg=4*int(math.sqrt(4))):
        print arg
