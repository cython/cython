# mode: run
# tag: genexpr, py3, py2

from __future__ import print_function

# Tests that function arguments to generator expressions are
# evaluated in the correct order (even after optimization)

import cython

@cython.cfunc
@cython.returns(cython.int)
def f():
    print(1)
    return 0

@cython.cfunc
@cython.returns(cython.int)
def g():
    print(2)
    return 5

@cython.test_assert_path_exists("//ForFromStatNode")
def genexp_range_argument_order():
    """
    >>> list(genexp_range_argument_order())
    1
    2
    [0, 1, 2, 3, 4]
    """
    return (a for a in range(f(), g()))

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_assert_path_exists(
    "//InlinedGeneratorExpressionNode",
    "//ComprehensionAppendNode")
def list_range_argument_order():
    """
    >>> list_range_argument_order()
    1
    2
    [0, 1, 2, 3, 4]
    """
    return list(a for a in range(f(), g()))

@cython.test_assert_path_exists("//ForFromStatNode")
def genexp_array_slice_order():
    """
    >>> list(genexp_array_slice_order())
    1
    2
    [0, 1, 2, 3, 4]
    """
    # TODO ideally find a way to add the evaluation of x to this test too
    x = cython.declare(cython.int[20], list(range(20)))
    return (a for a in x[f():g()])

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_assert_path_exists(
    "//InlinedGeneratorExpressionNode",
    "//ComprehensionAppendNode")
def list_array_slice_order():
    """
    >>> list(list_array_slice_order())
    1
    2
    [0, 1, 2, 3, 4]
    """
    # TODO ideally find a way to add the evaluation of x to this test too
    x = cython.declare(cython.int[20], list(range(20)))
    return list(a for a in x[f():g()])
