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

@cython.cfunc
@cython.returns(cython.int)
def h():
    print(3)
    return 1

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

class IndexableClass:
    def __getitem__(self, idx):
        print("In indexer")
        return [ idx.start, idx.stop, idx.step ]

class NoisyAttributeLookup:
    @property
    def indexer(self):
        print("Getting indexer")
        return IndexableClass()

    @property
    def function(self):
        print("Getting function")
        def func(a, b, c):
            print("In func")
            return [a, b, c]
        return func

def genexp_index_order():
    """
    >>> list(genexp_index_order())
    Getting indexer
    1
    2
    3
    In indexer
    Made generator expression
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    ret = (a for a in obj.indexer[f():g():h()])
    print("Made generator expression")
    return ret

@cython.test_assert_path_exists("//InlinedGeneratorExpressionNode")
def list_index_order():
    """
    >>> list_index_order()
    Getting indexer
    1
    2
    3
    In indexer
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    return list(a for a in obj.indexer[f():g():h()])


def genexpr_fcall_order():
    """
    >>> list(genexpr_fcall_order())
    Getting function
    1
    2
    3
    In func
    Made generator expression
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    ret = (a for a in obj.function(f(), g(), h()))
    print("Made generator expression")
    return ret

@cython.test_assert_path_exists("//InlinedGeneratorExpressionNode")
def list_fcall_order():
    """
    >>> list_fcall_order()
    Getting function
    1
    2
    3
    In func
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    return list(a for a in obj.function(f(), g(), h()))
