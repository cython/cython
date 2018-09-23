# mode: run
# cython: linetrace=True

cimport cython


@cython.test_fail_if_path_exists('//SwitchStatNode')
@cython.test_assert_path_exists('//IfStatNode')
def switch_simple_py(x):
    """
    >>> switch_simple_py(1)
    1
    >>> switch_simple_py(2)
    2
    >>> switch_simple_py(3)
    3
    >>> switch_simple_py(4)
    8
    >>> switch_simple_py(5)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in (4,):
        return 8
    else:
        return 0
    return -1


@cython.test_fail_if_path_exists('//SwitchStatNode')
@cython.test_assert_path_exists('//IfStatNode')
def switch_py(x):
    """
    >>> switch_py(1)
    1
    >>> switch_py(2)
    2
    >>> switch_py(3)
    3
    >>> switch_py(4)
    4
    >>> switch_py(5)
    4
    >>> switch_py(6)
    0
    >>> switch_py(8)
    4
    >>> switch_py(10)
    10
    >>> switch_py(12)
    12
    >>> switch_py(13)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    elif x in (10,11):
        return 10
    elif x in (12,):
        return 12
    else:
        return 0
    return -1


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def switch_simple_c(int x):
    """
    >>> switch_simple_c(1)
    1
    >>> switch_simple_c(2)
    2
    >>> switch_simple_c(3)
    3
    >>> switch_simple_c(4)
    8
    >>> switch_simple_c(5)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in (4,):
        return 8
    else:
        return 0
    return -1


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def switch_c(int x):
    """
    >>> switch_c(1)
    1
    >>> switch_c(2)
    2
    >>> switch_c(3)
    3
    >>> switch_c(4)
    4
    >>> switch_c(5)
    4
    >>> switch_c(6)
    0
    >>> switch_c(8)
    4
    >>> switch_c(10)
    10
    >>> switch_c(12)
    12
    >>> switch_c(13)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    elif x in [3]:
        return 3
    elif x in [4,5,7,8]:
        return 4
    elif x in (10,11):
        return 10
    elif x in (12,):
        return 12
    else:
        return 0
    return -1



@cython.test_assert_path_exists(
    '//SwitchStatNode',
    '//SwitchStatNode//SwitchStatNode',
)
@cython.test_fail_if_path_exists('//BoolBinopNode', '//PrimaryCmpNode')
def switch_in_switch(int x, int y):
    """
    >>> switch_in_switch(1, 1)
    (1, 1)
    >>> switch_in_switch(1, 2)
    (1, 2)
    >>> switch_in_switch(1, 4)
    (1, 3)

    >>> switch_in_switch(2, 1)
    (2, 1)
    >>> switch_in_switch(2, 2)
    (2, 2)
    >>> switch_in_switch(2, 3)
    (2, 3)
    >>> switch_in_switch(2, 4)
    (2, 4)
    >>> switch_in_switch(2, 20)
    (2, 4)

    >>> switch_in_switch(3, 0)
    False
    >>> switch_in_switch(3, 1)
    True
    >>> switch_in_switch(3, 2)
    True
    >>> switch_in_switch(3, 3)
    True
    >>> switch_in_switch(3, 4)
    False

    >>> switch_in_switch(20, 0)
    True
    >>> switch_in_switch(20, 1)
    False
    >>> switch_in_switch(20, 3)
    False
    >>> switch_in_switch(20, 4)
    True
    """
    if x == 1:
        if y == 1:
            return 1,1
        elif y == 2:
            return 1,2
        else:
            return 1,3
    elif x == 2:
        if y == 1:
            return 2,1
        elif y == 2:
            return 2,2
        elif y == 3:
            return 2,3
        else:
            return 2,4
    elif x == 3:
        return y in (1,2,3)
    else:
        return y not in (1,2,3)
    return 'FAILED'


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def switch_or(int x):
    """
    >>> switch_or(0)
    0
    >>> switch_or(1)
    1
    >>> switch_or(2)
    1
    >>> switch_or(3)
    1
    >>> switch_or(4)
    0
    """
    if x == 1 or x == 2 or x == 3:
        return 1
    else:
        return 0
    return -1


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def switch_in(int X):
    """
    >>> switch_in(0)
    0
    >>> switch_in(1)
    1
    >>> switch_in(2)
    0
    >>> switch_in(7)
    1
    >>> switch_in(8)
    0
    """
    if X in (1,3,5,7):
        return 1
    return 0


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def switch_short(int x):
    """
    >>> switch_short(0)
    0
    >>> switch_short(1)
    1
    >>> switch_short(2)
    2
    >>> switch_short(3)
    0
    """
    if x == 1:
        return 1
    elif 2 == x:
        return 2
    else:
        return 0
    return -1


@cython.test_fail_if_path_exists('//SwitchStatNode')
@cython.test_assert_path_exists('//IfStatNode')
def switch_off(int x):
    """
    >>> switch_off(0)
    0
    >>> switch_off(1)
    1
    >>> switch_off(2)
    0
    """
    if x == 1:
        return 1
    else:
        return 0
    return -1



@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def switch_pass(int x):
    """
    >>> switch_pass(1)
    1
    """
    if x == 1:
        pass
    elif x == 2:
        pass
    else:
        pass
    return x


DEF t = (1,2,3,4,5,6)

@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def compile_time_tuple_constant(int x):
    """
    >>> compile_time_tuple_constant(1)
    True
    >>> compile_time_tuple_constant(0)
    False
    >>> compile_time_tuple_constant(7)
    False
    """
    if x in t:
        return True
    else:
        return False


cdef enum X:
    a = 1
    b
    c
    d
    e = 10
    f = 100

@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def enum_switch(X x):
    """
    >>> enum_switch(1)
    0
    >>> enum_switch(10)
    1
    >>> enum_switch(100)
    2
    """
    if x in [a, b, c, d]:
        return 0
    elif x == e:
        return 1
    else:
        return 2


@cython.test_assert_path_exists('//IfStatNode')
@cython.test_assert_path_exists('//IfStatNode//SwitchStatNode')
def enum_duplicates(X x):
    """
    >>> enum_duplicates(1)
    0
    >>> enum_duplicates(2)  # b
    0
    >>> enum_duplicates(10)
    1
    >>> enum_duplicates(100)
    3
    """
    if x in [a, b, c, d]:   # switch is ok here!
        return 0
    elif x == e:
        return 1
    elif x == b:  # duplicate => no switch here!
        return 2
    else:
        return 3


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//IfStatNode')
def int_enum_switch_mix(int x):
    """
    >>> int_enum_switch_mix(1)
    0
    >>> int_enum_switch_mix(10)
    1
    >>> int_enum_switch_mix(ord('X'))
    2
    >>> int_enum_switch_mix(99)
    3
    >>> int_enum_switch_mix(100)
    4
    """
    if x in [a, b, c, d]:
        return 0
    elif x == e:
        return 1
    elif x == 'X':  # ASCII(88)
        return 2
    elif x == 99:
        return 3
    else:
        return 4


@cython.test_fail_if_path_exists('//SwitchStatNode')
@cython.test_assert_path_exists('//IfStatNode')
def int_enum_duplicates_mix(int x):
    """
    >>> int_enum_duplicates_mix(88)
    0
    >>> int_enum_duplicates_mix(ord('X'))
    0
    >>> int_enum_duplicates_mix(99)
    2
    >>> int_enum_duplicates_mix(100)
    3
    """
    if x == 88:
        return 0
    elif x == 'X':  # ASCII(88) => redundant
        return 1
    elif x == 99:
        return 2
    else:
        return 3


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//BoolBinopNode', '//PrimaryCmpNode')
def int_in_bool_binop(int x):
    """
    >>> int_in_bool_binop(0)
    False
    >>> int_in_bool_binop(1)
    True
    >>> int_in_bool_binop(2)
    True
    >>> int_in_bool_binop(3)
    False
    """
    return x == 1 or x == 2


@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//BoolBinopNode', '//PrimaryCmpNode')
def int_in_bool_binop_3(int x):
    """
    >>> int_in_bool_binop_3(0)
    False
    >>> int_in_bool_binop_3(1)
    True
    >>> int_in_bool_binop_3(2)
    True
    >>> int_in_bool_binop_3(3)
    False
    >>> int_in_bool_binop_3(4)
    True
    >>> int_in_bool_binop_3(5)
    False
    """
    return x == 1 or x == 2 or x == 4
