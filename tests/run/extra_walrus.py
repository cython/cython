# mode: run
# tag: pure3.8

# These are extra tests for the assignment expression/walrus operator/named expression that cover things
# additional to the standard Python test-suite in tests/run/test_named_expressions.pyx

import cython
import sys

@cython.test_assert_path_exists("//PythonCapiCallNode")
def optimized(x):
    """
    x*2 is optimized to a PythonCapiCallNode. The test fails unless the CloneNode is kept up-to-date
    (in the event that the optimization changes and test_assert_path_exists fails, the thing to do
    is to find another case that's similarly optimized - the test isn't specifically interested in
    multiplication)

    >>> optimized(5)
    10
    """
    return (x:=x*2)

# FIXME: currently broken; GH-4146
# Changing x in the assignment expression should not affect the value used on the right-hand side
#def order(x):
#    """
#    >>> order(5)
#    15
#    """
#    return x+(x:=x*2)

@cython.test_fail_if_path_exists("//CloneNode")
def optimize_literals1():
    """
    There's a small optimization for literals to avoid creating unnecessary temps
    >>> optimize_literals1()
    10
    """
    x = 5
    return (x := 10)

@cython.test_fail_if_path_exists("//CloneNode")
def optimize_literals2():
    """
    There's a small optimization for literals to avoid creating unnecessary temps
    Test is in __doc__ (for Py2 string formatting reasons)
    """
    x = 5
    return (x := u"a string")

@cython.test_fail_if_path_exists("//CloneNode")
def optimize_literals3():
    """
    There's a small optimization for literals to avoid creating unnecessary temps
    Test is in __doc__ (for Py2 string formatting reasons)
    """
    x = 5
    return (x := b"a bytes")

@cython.test_fail_if_path_exists("//CloneNode")
def optimize_literals4():
    """
    There's a small optimization for literals to avoid creating unnecessary temps
    Test is in __doc__ (for Py2 string formatting reasons)
    """
    x = 5
    return (x := (u"tuple", 1, 1.0, b"stuff"))

if sys.version_info[0] != 2:
    __doc__ = """
        >>> optimize_literals2()
        'a string'
        >>> optimize_literals3()
        b'a bytes'
        >>> optimize_literals4()
        ('tuple', 1, 1.0, b'stuff')
        """
else:
    __doc__ = """
        >>> optimize_literals2()
        u'a string'
        >>> optimize_literals3()
        'a bytes'
        >>> optimize_literals4()
        (u'tuple', 1, 1.0, 'stuff')
        """


@cython.test_fail_if_path_exists("//CoerceToPyTypeNode//AssignmentExpressionNode")
def avoid_extra_coercion(x : cython.double):
    """
    The assignment expression and x are both coerced to PyObject - this should happen only once
    rather than to both separately
    >>> avoid_extra_coercion(5.)
    5.0
    """
    y : object = "I'm an object"
    return (y := x)

async def async_func():
    """
    DW doesn't understand async functions well enough to make it a runtime test, but it was causing
    a compile-time failure at one point
    """
    if variable := 1:
        pass

y_global = 6

class InLambdaInClass:
    """
    >>> InLambdaInClass.x1
    12
    >>> InLambdaInClass.x2
    [12, 12]
    """
    x1 = (lambda y_global: (y_global := y_global + 1) + y_global)(2) + y_global
    x2 = [(lambda y_global: (y_global := y_global + 1) + y_global)(2) + y_global for _ in range(2) ]

def in_lambda_in_list_comprehension1():
    """
    >>> in_lambda_in_list_comprehension1()
    [[0, 2, 4, 6], [0, 2, 4, 6], [0, 2, 4, 6], [0, 2, 4, 6], [0, 2, 4, 6]]
    """
    return [ (lambda x: [(x := y) + x for y in range(4)])(x) for x in range(5) ]

def in_lambda_in_list_comprehension2():
    """
    >>> in_lambda_in_list_comprehension2()
    [[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]]
    """
    return [ (lambda z: [(x := y) + z for y in range(4)])(x) for x in range(5) ]

def in_lambda_in_generator_expression1():
    """
    >>> in_lambda_in_generator_expression1()
    [(0, 2, 4, 6), (0, 2, 4, 6), (0, 2, 4, 6), (0, 2, 4, 6), (0, 2, 4, 6)]
    """
    return [ (lambda x: tuple((x := y) + x for y in range(4)))(x) for x in range(5) ]

def in_lambda_in_generator_expression2():
    """
    >>> in_lambda_in_generator_expression2()
    [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5), (3, 4, 5, 6), (4, 5, 6, 7)]
    """
    return [ (lambda z: tuple((x := y) + z for y in range(4)))(x) for x in range(5) ]
