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

    >>> optimize_literals2()
    'a string'
    """
    x = 5
    return (x := u"a string")


@cython.test_fail_if_path_exists("//CloneNode")
def optimize_literals3():
    """
    There's a small optimization for literals to avoid creating unnecessary temps

    >>> optimize_literals3()
    b'a bytes'
    """
    x = 5
    return (x := b"a bytes")


@cython.test_fail_if_path_exists("//CloneNode")
def optimize_literals4():
    """
    There's a small optimization for literals to avoid creating unnecessary temps

    >>> optimize_literals4()
    ('tuple', 1, 1.0, b'stuff')
    """
    x = 5
    return (x := (u"tuple", 1, 1.0, b"stuff"))


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


# A bunch of tests where assignment may/may not happen and flow control has to
# be able to detect this to avoid crashing:

def flow_control_binops1(test, value):
    """
    >>> flow_control_binops1(True, "value")
    ('value', 'value')
    >>> flow_control_binops1(False, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    res = test and (target := value)

    return res, target

def flow_control_binops2(test, value):
    """
    >>> flow_control_binops2(True, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    >>> flow_control_binops2(False, "value")
    ('value', 'value')
    """
    res = test or (target := value)

    return res, target

def flow_control_binops3(test, value):
    """
    >>> flow_control_binops3(True, "value")
    ('value', 'value')
    >>> flow_control_binops3(False, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    # "True" may or may not be optimized out here
    # but either way the assignment is uncertain
    res = True and test and (target := value)

    return res, target

def flow_control_binops4(test1, test2, value):
    """
    >>> flow_control_binops4(True, True, "value")
    ('value', 'value')
    >>> flow_control_binops4(False, True, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    >>> flow_control_binops4(False, False, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    >>> flow_control_binops4(True, False, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    # "True" may or may not be optimized out here
    # but either way the assignment is uncertain
    res = test1 and test2 and (target := value)

    return res, target

def flow_control_cond_expr1(test, value):
    """
    >>> flow_control_cond_expr1(True, "value")
    ('value', 'value')
    >>> flow_control_cond_expr1(False, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    res = (target := value) if test else None
    return res, target

def flow_control_cond_expr2(test, value):
    """
    >>> flow_control_cond_expr2(True, "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    >>> flow_control_cond_expr2(False, "value")
    ('value', 'value')
    """
    res = None if test else (target := value)
    return res, target

def flow_control_cond_expr3(test, value1, value2):
    """
    >>> flow_control_cond_expr3(True, "value1", "value2")
    ('value1', 'value1')
    >>> flow_control_cond_expr3(False, "value1", "value2")
    ('value2', 'value2')
    """
    res = (target := value1) if test else (target := value2)
    # Not tested here (but I believe working) - Cython shouldn't need
    # to generate an unbound local check for "target"
    return res, target

def flow_control_list_comp(it, value):
    """
    >>> flow_control_list_comp([1], "value")
    'value'
    >>> flow_control_list_comp([], "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    [(target := value) for _ in it]
    return target

def flow_control_set_comp(it, value):
    """
    >>> flow_control_set_comp([1], "value")
    'value'
    >>> flow_control_set_comp([], "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    {(target := value) for _ in it}
    return target

def flow_control_dict_comp1(it, value):
    """
    >>> flow_control_dict_comp1([1], "value")
    'value'
    >>> flow_control_dict_comp1([], "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    {(target := value): x for x in it}
    return target

def flow_control_dict_comp2(it, value):
    """
    >>> flow_control_dict_comp2([1], "value")
    'value'
    >>> flow_control_dict_comp2([], "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    {x: (target := value) for x in it}
    return target

def flow_control_genexp(it, value):
    """
    >>> flow_control_genexp([1], "value")
    'value'
    >>> flow_control_genexp([], "value")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnboundLocalError
    """
    all((target := value) for _ in it)
    return target

def memoryview_walrus(x: cython.uchar[:]):
    """
    >>> memoryview_walrus(bytearray(b"123"))
    '1'
    """
    (y := x)
    return chr(y[0])
