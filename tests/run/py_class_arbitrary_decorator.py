# mode: run
# tag: decorator
# tag: pure2.0 pure3.0
# Github #1434 #1274
#cython: binding=True

# substantially just a copy of "cdef_class_arbitrary_decorator" but
# with a Python class instead of a cdef class

from __future__ import print_function

import cython

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

class C:
    """
    For cm1:
    Should fail with a TypeError (the exact error is version specific though)
    >>> C.cm1(1, 2, 3)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: 'classmethod' object is not callable
    >>> C().cm1(1, 2, 3)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: 'classmethod' object is not callable

    For cm2:
    Should work correctly
    >>> C.cm2(1, 2, 3)
    7
    >>> C().cm2(1, 2, 3)
    7

    sm1 behaves differently Python 3.10+ (on both Python and Cython)
    and thus is tested in the module __doc__

    For sm2:
    Should work correctly
    >>> C.sm2(1, 2, 3)
    7
    >>> C().sm2(1, 2, 3)
    7

    arb_decorated1 and arb_decorated2 are version dependent so in the module __doc__
    """
    def imag(self):
        # named because int has an attribute `imag` so we can test
        # what type we're being passed. Less interesting than for the
        # cdef class version because the call isn't resolved at compile-time
        return 100

    @add1_dec
    @classmethod
    def cm1(cls, *vals):
        return int(cls == C)*sum(vals)

    @classmethod
    @add1_dec
    def cm2(cls, *vals):
        return int(cls == C)*sum(vals)

    @add1_dec
    @staticmethod
    def sm1(*vals):
        return int(not isinstance(vals[0], C))*sum(vals)

    @staticmethod
    @add1_dec
    def sm2(*vals):
        return int(not isinstance(vals[0], C))*sum(vals)

    @arbitrary_decorator1
    def arb_decorated1(self, *args):
        print(cython.typeof(self), type(self).__name__)
        print(self.imag(), sum(args))

    @arbitrary_decorator2
    def arb_decorated2(not_self, *args):
        print(cython.typeof(not_self), type(not_self).__name__)
        print(type(args[0]).__name__)
        print(not_self.imag, sum(args[1:]))

    @arbitrary_decorator1
    def arb_decorated3(*args):
        print(cython.typeof(args), type(args).__name__)
        print(type(args[0]).__name__, sum(args[1:]))

import sys

__doc__ = """
    For arb_decorated1
    >>> C().arb_decorated1(1,2,3)
    {4} {0}
    100 6
    >>> C.arb_decorated1(C(), 1,2,3)
    {4} {0}
    100 6
    >>> C.arb_decorated1(1, 1,2,3) {3}
    Traceback (most recent call last):
    TypeError: {2}

    For arb_decorated2
    >>> C().arb_decorated2(1,2,3)
    {1} int
    {0}
    0 6
    >>> C.arb_decorated2(C(), 1,2,3)
    {1} int
    {0}
    0 6

    For arb_decorated3
    >>> C().arb_decorated3(1, 2, 3)
    tuple{5} tuple
    {0} 6
    """.format(
        "C" if sys.version_info[0] > 2 else "instance",
        "Python object" if cython.compiled else "int",
        "'int' object is not callable" if sys.version_info[0] > 2 else "unbound method",
        # exact detail vary depending on if it's compiled...
        "" if sys.version_info[0] > 2 else "# doctest: +IGNORE_EXCEPTION_DETAIL",
        "Python object" if cython.compiled else "C",
        " object" if cython.compiled else "",
        )

if sys.version_info < (3, 10):
    __doc__ += """
    For sm1:
    Should fail with a TypeError
    >>> C.sm1(1, 2, 3)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: 'staticmethod' object is not callable
    >>> C().sm1(1, 2, 3)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: 'staticmethod' object is not callable
    """
else:
    # Python 3.10 made staticmethod instances callable like any other function
    # and thus sm1 works
    __doc__ += """
    >>> C.sm1(1, 2, 3)
    7

    Don't test C().sm1(1, 2, 3) - it equals C.sm1(C(), 1, 2, 3). Which is "correct"
    but not hugely useful.
    """
