# mode: run
# tag: pure3.8

# These are extra tests for the assignment expression/walrus operator/named expression that cover things
# additional to the standard Python test-suite in tests/run/test_named_expressions.pyx

import cython

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
def optimize_literals():
    """
    There's a small optimization for literals to avoid creating unnecessary temps
    >>> optimize_literals()
    10
    """
    x = 5
    return (x := 10)

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
