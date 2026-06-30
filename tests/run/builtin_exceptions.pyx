# mode: run
# tag: builtins, exceptions
# cython: language_level=3

import cython


def test_isinstance():
    """
    >>> test_isinstance()
    Exception True
    BaseException True
    KeyError/BaseException True
    KeyError/Exception True
    KeyError/KeyError True
    Exception/KeyError False
    """
    print("Exception", isinstance(Exception(), Exception))
    print("BaseException", isinstance(Exception(), BaseException))
    print("KeyError/BaseException", isinstance(KeyError(), BaseException))
    print("KeyError/Exception", isinstance(KeyError(), Exception))
    print("KeyError/KeyError", isinstance(KeyError(), KeyError))
    print("Exception/KeyError", isinstance(Exception(), KeyError))


def test_hierarchy_inference(x):
    """
    >>> test_hierarchy_inference(True)
    BaseException object
    Exception object
    ArithmeticError object
    """

    base_exc = BaseException() if x else Exception()
    print(cython.typeof(base_exc))

    exc = Exception() if x else KeyError()
    print(cython.typeof(exc))

    arith_exc = FloatingPointError() if x else OverflowError()
    print(cython.typeof(arith_exc))
