# mode: run
# tag: decorator
# Github #1434 #1274
#cython: binding=True

from __future__ import print_function

cimport cython

def add1_dec(func):
    def add1(*args, **kwds):
        return func(*args, **kwds)+1
    return add1

def arbitrary_decorator1(func):
    def wrapper(*args):
        return func(*args)
    return wrapper

def arbitrary_decorator2(func):
    # note that it passes an int as the first object
    def wrapper(*args):
        return func(1, *args)
    return wrapper

cdef class C:
    cdef int imag(self):
        # named because int has an attribute `imag` so we can test
        # what type we're getting
        return 100

    @add1_dec
    @classmethod
    def cm1(cls, *vals):
        """
        Should fail with a TypeError
        >>> C.cm1(1, 2, 3)
        Traceback (most recent call last):
        TypeError: 'classmethod' object is not callable
        >>> C().cm1(1, 2, 3)
        Traceback (most recent call last):
        TypeError: 'classmethod' object is not callable
        """
        return int(isinstance(cls, type))*sum(vals)

    @classmethod
    @add1_dec
    def cm2(cls, *vals):
        """
        Should work correctly
        >>> C.cm2(1, 2, 3)
        7
        >>> C().cm2(1, 2, 3)
        7
        """
        return int(isinstance(cls, type))*sum(vals)

    @add1_dec
    @staticmethod
    def sm1(*vals):
        """
        Should fail with a TypeError
        >>> C.sm1(1, 2, 3)  # doctest:
        Traceback (most recent call last):
        TypeError: 'staticmethod' object is not callable
        >>> C().sm1(1, 2, 3)  # doctest:
        Traceback (most recent call last):
        TypeError: 'staticmethod' object is not callable
        """
        return int(not isinstance(vals[0], C))*sum(vals)

    @staticmethod
    @add1_dec
    def sm2(*vals):
        """
        Should work correctly
        >>> C.sm2(1, 2, 3)
        7
        >>> C().sm2(1, 2, 3)
        7
        """
        return int(not isinstance(vals[0], C))*sum(vals)

    @arbitrary_decorator1
    def arb_decorated1(self, *args):
        """
        >>> C().arb_decorated1(1,2,3)
        C C
        100 6
        >>> C.arb_decorated1(C(), 1,2,3)
        C C
        100 6
        """
        print(cython.typeof(self), type(self).__name__)
        print(self.imag(), sum(args))

    @arbitrary_decorator2
    def arb_decorated2(not_self, *args):
        """
        >>> C().arb_decorated2(1,2,3)
        Python object int
        C
        0 6
        >>> C.arb_decorated2(C(), 1,2,3)
        Python object int
        C
        0 6
        """
        print(cython.typeof(not_self), type(not_self).__name__)
        print(type(args[0]).__name__)
        print(not_self.imag, sum(args[1:]))
