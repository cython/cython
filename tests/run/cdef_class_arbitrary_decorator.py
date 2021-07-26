# mode: run
# tag: decorator
# tag: pure2.0, pure3.0
# Github #1434 #1274
#cython: binding=True, fused_types_arbitrary_decorators=True

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

@cython.cclass
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
    @cython.cfunc
    @cython.returns(cython.int)
    def imag(self):
        # named because int has an attribute `imag` so we can test
        # what type we're getting
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

    @cython.test_assert_path_exists("//FusedCFuncDefNode")  # because of the arbitrary decorator
        # this should internally be transformed to a fused function
    @arbitrary_decorator1
    def arb_decorated1(self, *args):
        print(cython.typeof(self), type(self).__name__)
        print(self.imag(), sum(args))

    @cython.test_fail_if_path_exists("//FusedCFuncDefNode")  # since we've specified a type
        # the fused node isn't generated
    @arbitrary_decorator1
    @cython.locals(self="C")
    def arb_decorated1_typed(self, *args):
        print(cython.typeof(self), type(self).__name__)
        print(self.imag(), sum(args))

    @cython.test_assert_path_exists("//FusedCFuncDefNode")
    @arbitrary_decorator2
    def arb_decorated2(not_self, *args):
        print(cython.typeof(not_self), type(not_self).__name__)
        print(type(args[0]).__name__)
        print(not_self.imag, sum(args[1:]))

    @cython.test_fail_if_path_exists("//FusedCFuncDefNode")  # args is know to be a tuple so
        # should not need a fused function
    @arbitrary_decorator1
    def arb_decorated3(*args):
        print(cython.typeof(args), type(args).__name__)
        print(type(args[0]).__name__, sum(args[1:]))

@cython.cclass
@cython.fused_types_arbitrary_decorators(False)
class D:
    # should also generate a warning (not tested)
    @cython.test_fail_if_path_exists("//FusedCFuncDefNode")
    @arbitrary_decorator1
    def arb_decorated1(self, *args):
        print(cython.typeof(self), type(self).__name__)
        print(self.imag(), sum(args))

    # no warning
    @cython.test_fail_if_path_exists("//FusedCFuncDefNode")
    @arbitrary_decorator1
    @cython.locals(self="C")
    def arb_decorated1_typed(self, *args):
        print(cython.typeof(self), type(self).__name__)
        print(self.imag(), sum(args))

import sys

__doc__ = """
    For arb_decorated1
    >>> C().arb_decorated1(1,2,3)
    C {0}
    100 6
    >>> C.arb_decorated1(C(), 1,2,3)
    C {0}
    100 6
    >>> C.arb_decorated1(1, 1,2,3) {3}
    Traceback (most recent call last):
    TypeError: {2}


    For arb_decorated1_typed behaves much like arg_decorated1
    (except that the call passing an int will be dangerous)
    >>> C().arb_decorated1_typed(1,2,3)
    C {0}
    100 6
    >>> C.arb_decorated1_typed(C(), 1,2,3)
    C {0}
    100 6

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
    tuple{4} tuple
    {0} 6
    """.format(
        "C" if sys.version_info[0] > 2 or cython.compiled else "instance",
        "Python object" if cython.compiled else "int",
        "'int' object is not callable" if sys.version_info[0] > 2 else "unbound method",
        # exact detail vary depending on if it's compiled...
        "" if sys.version_info[0] > 2 else "# doctest: +IGNORE_EXCEPTION_DETAIL",
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
    >>> C().sm1(1, 2, 3)
    7
    """
