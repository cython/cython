# mode: run
# tag: genexpr, py3, py2

from __future__ import print_function

# Tests that function arguments to generator expressions are
# evaluated in the correct order (even after optimization)
# WARNING: there may be an amount of luck in this working correctly (since it
# isn't strictly enforced). Therefore perhaps be prepared to disable these
# tests if they stop working and aren't easily fixed

import cython

@cython.cfunc
@cython.returns(cython.int)
def zero():
    print("In zero")
    return 0

@cython.cfunc
@cython.returns(cython.int)
def five():
    print("In five")
    return 5

@cython.cfunc
@cython.returns(cython.int)
def one():
    print("In one")
    return 1

# FIXME - I don't think this is easy to enforce unfortunately, but it is slightly wrong
#@cython.test_assert_path_exists("//ForFromStatNode")
#def genexp_range_argument_order():
#    """
#    >>> list(genexp_range_argument_order())
#    In zero
#    In five
#    [0, 1, 2, 3, 4]
#    """
#    return (a for a in range(zero(), five()))
#
#@cython.test_assert_path_exists("//ForFromStatNode")
#@cython.test_assert_path_exists(
#    "//InlinedGeneratorExpressionNode",
#    "//ComprehensionAppendNode")
#def list_range_argument_order():
#    """
#    >>> list_range_argument_order()
#    In zero
#    In five
#    [0, 1, 2, 3, 4]
#    """
#    return list(a for a in range(zero(), five()))

@cython.test_assert_path_exists("//ForFromStatNode")
def genexp_array_slice_order():
    """
    >>> list(genexp_array_slice_order())
    In zero
    In five
    [0, 1, 2, 3, 4]
    """
    # TODO ideally find a way to add the evaluation of x to this test too
    x = cython.declare(cython.int[20])
    x = list(range(20))
    return (a for a in x[zero():five()])

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_assert_path_exists(
    "//InlinedGeneratorExpressionNode",
    "//ComprehensionAppendNode")
def list_array_slice_order():
    """
    >>> list(list_array_slice_order())
    In zero
    In five
    [0, 1, 2, 3, 4]
    """
    # TODO ideally find a way to add the evaluation of x to this test too
    x = cython.declare(cython.int[20])
    x = list(range(20))
    return list(a for a in x[zero():five()])

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
    In zero
    In five
    In one
    In indexer
    Made generator expression
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    ret = (a for a in obj.indexer[zero():five():one()])
    print("Made generator expression")
    return ret

@cython.test_assert_path_exists("//InlinedGeneratorExpressionNode")
def list_index_order():
    """
    >>> list_index_order()
    Getting indexer
    In zero
    In five
    In one
    In indexer
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    return list(a for a in obj.indexer[zero():five():one()])


def genexpr_fcall_order():
    """
    Note that the order of getting the function and evaluating the
    function arguments can end up slightly different in Python and
    Cython and so isn't tested.

    >>> list(genexpr_fcall_order())
    Getting function
    In func
    Made generator expression
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    ret = (a for a in obj.function(0, 5, 1))
    print("Made generator expression")
    return ret

@cython.test_assert_path_exists("//InlinedGeneratorExpressionNode")
def list_fcall_order():
    """
    Note that the order of getting the function and evaluating the
    function arguments can end up slightly different in Python and
    Cython and so isn't tested.

    >>> list_fcall_order()
    Getting function
    In func
    [0, 5, 1]
    """
    obj = NoisyAttributeLookup()
    return list(a for a in obj.function(0, 5, 1))

def call1():
    print("In call1")
    return ["a"]
def call2():
    print("In call2")
    return ["b"]

def multiple_genexps_to_call_order():
    """
    >>> multiple_genexps_to_call_order()
    In call1
    In call2
    """
    def takes_two_genexps(a, b):
        pass

    return takes_two_genexps((x for x in call1()), (x for x in call2()))
