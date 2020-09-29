import sys
IS_PY3 = sys.version_info[0] >= 3

cimport cython

DEF INT_VAL = 1

def _func(a,b,c):
    return a+b+c

@cython.test_fail_if_path_exists("//AddNode")
def add():
    """
    >>> add() == 1+2+3+4
    True
    """
    return 1+2+3+4

#@cython.test_fail_if_path_exists("//AddNode")
def add_var(a):
    """
    >>> add_var(10) == 1+2+10+3+4
    True
    """
    return 1+2 +a+ 3+4

@cython.test_fail_if_path_exists("//AddNode", "//SubNode")
def neg():
    """
    >>> neg() == -1 -2 - (-3+4)
    True
    """
    return -1 -2 - (-3+4)

@cython.test_fail_if_path_exists("//AddNode", "//MulNode", "//DivNode")
def long_int_mix():
    """
    >>> long_int_mix() == 1 + (2 * 3) // 2
    True
    >>> if IS_PY3: type(long_int_mix()) is int  or type(long_int_mix())
    ... else:      type(long_int_mix()) is long or type(long_int_mix())
    True
    """
    return 1L + (2 * 3L) // 2

@cython.test_fail_if_path_exists("//AddNode", "//MulNode", "//DivNode")
def char_int_mix():
    """
    >>> char_int_mix() == 1 + (ord(' ') * 3) // 2 + ord('A')
    True
    """
    return 1L + (c' ' * 3L) // 2 + c'A'

@cython.test_fail_if_path_exists("//AddNode", "//MulNode")
def int_cast():
    """
    >>> int_cast() == 1 + 2 * 6000
    True
    """
    return <int>(1 + 2 * 6000)

@cython.test_fail_if_path_exists("//MulNode")
def mul():
    """
    >>> mul() == 1*60*1000
    True
    """
    return 1*60*1000

@cython.test_fail_if_path_exists("//AddNode", "//MulNode")
def arithm():
    """
    >>> arithm() == 9*2+3*8//6-10
    True
    """
    return 9*2+3*8//6-10

@cython.test_fail_if_path_exists("//AddNode", "//MulNode")
def parameters():
    """
    >>> parameters() == _func(-1 -2, - (-3+4), 1*2*3)
    True
    """
    return _func(-1 -2, - (-3+4), 1*2*3)

#@cython.test_fail_if_path_exists("//AddNode")
def lists():
    """
    >>> lists() == [1,2,3] + [4,5,6]
    True
    """
    return [1,2,3] + [4,5,6]

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_right_len1():
    """
    >>> multiplied_lists_right_len1() == [1] * 5
    True
    """
    return [1] * 5

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_right():
    """
    >>> multiplied_lists_right() == [1,2,3] * 5
    True
    """
    return [1,2,3] * 5

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_left():
    """
    >>> multiplied_lists_left() == [1,2,3] * 5
    True
    """
    return 5 * [1,2,3]

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_neg():
    """
    >>> multiplied_lists_neg() == [1,2,3] * -5
    True
    """
    return [1,2,3] * -5

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_nonconst(x):
    """
    >>> multiplied_lists_nonconst(5) == [1,2,3] * 5
    True
    >>> multiplied_lists_nonconst(-5) == [1,2,3] * -5
    True
    >>> multiplied_lists_nonconst(0) == [1,2,3] * 0
    True

    >>> try: [1,2,3] * 'abc'
    ... except TypeError: pass
    >>> try: multiplied_nonconst_tuple_arg('abc')
    ... except TypeError: pass
    >>> try: [1,2,3] * 1.0
    ... except TypeError: pass
    >>> try: multiplied_nonconst_tuple_arg(1.0)
    ... except TypeError: pass
    """
    return [1,2,3] * x

@cython.test_assert_path_exists("//MulNode")
def multiplied_lists_nonconst_left(x):
    """
    >>> multiplied_lists_nonconst_left(5) == 5 * [1,2,3]
    True
    >>> multiplied_lists_nonconst_left(-5) == -5 * [1,2,3]
    True
    >>> multiplied_lists_nonconst_left(0) == 0 * [1,2,3]
    True
    """
    return x * [1,2,3]

@cython.test_fail_if_path_exists("//MulNode//ListNode")
@cython.test_assert_path_exists("//MulNode")
def multiplied_lists_nonconst_expression(x):
    """
    >>> multiplied_lists_nonconst_expression(5) == [1,2,3] * (5 * 2)
    True
    >>> multiplied_lists_nonconst_expression(-5) == [1,2,3] * (-5 * 2)
    True
    >>> multiplied_lists_nonconst_expression(0) == [1,2,3] * (0 * 2)
    True
    """
    return [1,2,3] * (x*2)

cdef side_effect(int x):
    print x
    return x

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_with_side_effects():
    """
    >>> multiplied_lists_with_side_effects() == [1,2,3] * 5
    1
    2
    3
    True
    """
    return [side_effect(1), side_effect(2), side_effect(3)] * 5

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_lists_nonconst_with_side_effects(x):
    """
    >>> multiplied_lists_nonconst_with_side_effects(5) == [1,2,3] * 5
    1
    2
    3
    True
    """
    return [side_effect(1), side_effect(2), side_effect(3)] * x

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_nonconst_tuple_arg(x):
    """
    >>> multiplied_nonconst_tuple_arg(5) == (1,2) * 5
    True
    >>> multiplied_nonconst_tuple_arg(-5) == (1,2) * -5
    True
    >>> multiplied_nonconst_tuple_arg(0) == (1,2) * 0
    True

    >>> try: (1,2) * 'abc'
    ... except TypeError: pass
    >>> try: multiplied_nonconst_tuple_arg('abc')
    ... except TypeError: pass
    >>> try: (1,2) * 1.0
    ... except TypeError: pass
    >>> try: multiplied_nonconst_tuple_arg(1.0)
    ... except TypeError: pass
    """
    return (1,2) * x

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_nonconst_tuple_int_arg(int x):
    """
    >>> multiplied_nonconst_tuple_int_arg(5) == (1,2) * 5
    True
    """
    return (1,2) * x

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_nonconst_tuple(x):
    """
    >>> multiplied_nonconst_tuple(5) == (1,2) * (5+1)
    True
    """
    return (1,2) * (x + 1)

MULT = 5

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_global_nonconst_tuple():
    """
    >>> multiplied_global_nonconst_tuple() == (1,2,3) * 5
    1
    2
    3
    True
    """
    return (side_effect(1), side_effect(2), side_effect(3)) * MULT

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_const_tuple():
    """
    >>> multiplied_const_tuple() == (1,2) * 5
    True
    """
    return (1,2) * 5

@cython.test_fail_if_path_exists("//MulNode")
def multiplied_const_tuple_len1():
    """
    >>> multiplied_const_tuple_len1() == (1,) * 5
    True
    """
    return (1,) * 5

@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def compile_time_DEF():
    """
    >>> compile_time_DEF()
    (1, False, True, True, False)
    """
    return INT_VAL, INT_VAL == 0, INT_VAL != 0, INT_VAL == 1, INT_VAL != 1

@cython.test_fail_if_path_exists("//PrimaryCmpNode")
def cascaded_compare():
    """
    >>> cascaded_compare()
    True
    """
    return 1 < 2 < 3 < 4
