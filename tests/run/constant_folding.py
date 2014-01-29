# coding=utf8
# mode: run
# tag: constant_folding

import cython


@cython.test_fail_if_path_exists(
    "//UnaryMinusNode",
    "//UnaryPlusNode",
)
def unop_floats():
    """
    >>> unop_floats()
    (False, 2.0, -2.0, False, 2.0, -2.0, -2.0)
    """
    not1   = not 2.0
    plus1  = + 2.0
    minus1 = - 2.0
    not3   = not not not 2.0
    plus3  = +++ 2.0
    minus3 = --- 2.0
    mix    = +-++-- 2.0
    return not1, plus1, minus1, not3, plus3, minus3, mix


@cython.test_fail_if_path_exists(
    "//UnaryMinusNode",
    "//UnaryPlusNode",
    "//CoerceToPyTypeNode",
)
def unop_py_floats_tuple():
    """
    >>> unop_floats()
    (False, 2.0, -2.0, False, 2.0, -2.0, -2.0)
    """
    return (
        not 2.0,
        + 2.0,
        - 2.0,
        not not not 2.0,
        +++ 2.0,
        --- 2.0,
        +-++-- 2.0)


@cython.test_fail_if_path_exists(
    "//UnaryMinusNode",
    "//UnaryPlusNode",
)
def unop_ints():
    """
    >>> unop_ints()
    (False, 2, -2, False, 2, -2, -2)
    """
    not1   = not 2
    plus1  = + 2
    minus1 = - 2
    not3   = not not not 2
    plus3  = +++ 2
    minus3 = --- 2
    mix    = +-++-- 2
    return not1, plus1, minus1, not3, plus3, minus3, mix


@cython.test_fail_if_path_exists(
    "//UnaryMinusNode",
    "//UnaryPlusNode",
    "//NotNode",
)
def unop_bool():
    """
    >>> unop_bool()
    (False, 1, -1, False, 1, -1, -1)
    """
    not1   = not True
    plus1  = + True
    minus1 = - True
    not3   = not not not True
    plus3  = +++ True
    minus3 = --- True
    mix    = +-++-- True
    return not1, plus1, minus1, not3, plus3, minus3, mix


@cython.test_fail_if_path_exists(
    "//AddNode",
    "//SubNode",
)
def binop_bool():
    """
    >>> binop_bool()
    (2, 1, 0, True, True, 1, False, 2, 2, -2, False, True, 1, False)
    """
    plus1  = True + True
    pmix1  = True + 0
    minus1 = True - True
    and1   = True & True
    or1    = True | True
    ormix1 = True | 0
    xor1   = True ^ True
    plus3  = False + True + False + True
    pmix3  = False + True + 0 + True
    minus3 = False - True - False - True
    and3   = False & True & False & True
    or3    = False | True | False | True
    ormix3 = False | 0 | False | True
    xor3   = False ^ True ^ False ^ True
    return plus1, pmix1, minus1, and1, or1, ormix1, xor1, plus3, pmix3, minus3, and3, or3, ormix3, xor3


@cython.test_fail_if_path_exists(
    "//SliceIndexNode",
)
def slicing2():
    """
    >>> slicing2()
    ([1, 2, 3, 4], [3, 4], [1, 2, 3, 4], [3, 4], (1, 2, 3, 4), (3, 4), (1, 2, 3, 4), (3, 4))
    """
    lst0 = [1, 2, 3, 4][:]
    lst1 = [1, 2, 3, 4][2:]
    lst2 = [1, 2, 3, 4][:4]
    lst3 = [1, 2, 3, 4][2:4]

    tpl0 = (1, 2, 3, 4)[:]
    tpl1 = (1, 2, 3, 4)[2:]
    tpl2 = (1, 2, 3, 4)[:4]
    tpl3 = (1, 2, 3, 4)[2:4]

    return lst0, lst1, lst2, lst3, tpl0, tpl1, tpl2, tpl3


@cython.test_fail_if_path_exists(
    "//SliceIndexNode",
)
def str_slicing2():
    """
    >>> a,b,c,d = str_slicing2()
    >>> a == 'abc\\xE9def'[:]
    True
    >>> b == 'abc\\xE9def'[2:]
    True
    >>> c == 'abc\\xE9def'[:4]
    True
    >>> d == 'abc\\xE9def'[2:4]
    True
    """
    str0 = 'abc\xE9def'[:]
    str1 = 'abc\xE9def'[2:]
    str2 = 'abc\xE9def'[:4]
    str3 = 'abc\xE9def'[2:4]

    return str0, str1, str2, str3


@cython.test_fail_if_path_exists(
    "//IfStatNode",
)
def str_in_and_not_in():
    """
    >>> str_in_and_not_in()
    True
    """
    if 'a' in 'abc' and 'b' in 'abc' and 'c' in 'abc' and 'd' not in 'abc': return True
    else: return False


@cython.test_fail_if_path_exists(
    "//WhileStatNode",
)
def while_false():
    """
    >>> while_false()
    """
    while 1 == 0:
        return False


@cython.test_fail_if_path_exists(
    "//WhileStatNode",
    )
def while_false_else():
    """
    >>> while_false_else()
    True
    """
    while 1 == 0:
        return False
    else:
        return True


@cython.test_fail_if_path_exists(
    "//WhileStatNode//PrintStatNode",
    "//WhileStatNode//PrimaryCmpNode",
    "//WhileStatNode/BoolNode",
    "//WhileStatNode/IntNode",
)
@cython.test_assert_path_exists(
    "//WhileStatNode",
)
def while_true():
    """
    >>> while_true()
    True
    """
    while 1 == 1:
        return True
    else:
        print("FAIL")


@cython.test_fail_if_path_exists(
    "//ForInStatNode",
)
def for_in_empty():
    """
    >>> for_in_empty()
    """
    for i in []:
        print("LOOP")


@cython.test_fail_if_path_exists(
    "//ForInStatNode",
)
def for_in_empty_else():
    """
    >>> for_in_empty_else()
    True
    """
    for i in []:
        print("LOOP")
    else:
        return True


@cython.test_fail_if_path_exists(
    "//ComprehensionNode",
    "//ForInStatNode",
)
@cython.test_assert_path_exists(
    "//ListNode",
)
def for_in_empty_listcomp():
    """
    >>> for_in_empty_listcomp()
    []
    """
    return [i for i in []]


@cython.test_fail_if_path_exists(
    "//ComprehensionNode",
    "//ForInStatNode",
)
@cython.test_assert_path_exists(
    "//ListNode",
)
def for_in_empty_nested_listcomp():
    """
    >>> for_in_empty_nested_listcomp()
    []
    """
    return [x for _ in [] for x in [1, 2, 3]]


@cython.test_fail_if_path_exists(
    "//ForInStatNode//ForInStatNode",
)
@cython.test_assert_path_exists(
    "//ForInStatNode",
    "//ComprehensionNode",
)
def for_in_nested_listcomp():
    """
    >>> for_in_nested_listcomp()
    []
    """
    return [x for x in [1, 2, 3] for _ in []]


@cython.test_fail_if_path_exists(
    "//MulNode",
)
def mult_empty_list():
    """
    >>> mult_empty_list()
    []
    """
    return 5 * [] * 100


@cython.test_fail_if_path_exists(
    "//MulNode",
)
def mult_list_int_int():
    """
    >>> mult_list_int_int()
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    """
    return [1, 2] * 2 * 3


@cython.test_fail_if_path_exists(
    "//MulNode",
)
def mult_int_list_int():
    """
    >>> mult_int_list_int()
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    """
    return 3 * [1, 2] * 2


@cython.test_fail_if_path_exists(
    "//MulNode",
    "//ListNode//IntNode",
)
def neg_mult_list():
    """
    >>> neg_mult_list()
    []
    """
    return -5 * [1, 2] * -100


@cython.test_fail_if_path_exists(
    "//MulNode",
    "//ListNode//IntNode",
)
def zero_mult_list():
    """
    >>> zero_mult_list()
    []
    """
    return 0 * [1, 2] * 0


@cython.test_assert_path_exists(
    "//BoolNode",
)
@cython.test_fail_if_path_exists(
    "//PrimaryCmpNode",
    "//MulNode",
    "//ListNode//IntNode",
)
def in_mult_list():
    """
    >>> in_mult_list()
    False
    """
    return 5 in 100 * [1, 2] * 0


@cython.test_assert_path_exists(
    "//BoolNode",
)
@cython.test_fail_if_path_exists(
    "//PrimaryCmpNode",
    "//MulNode",
    "//ListNode//IntNode",
)
def not_in_mult_list():
    """
    >>> not_in_mult_list()
    True
    """
    return 5 not in 100 * [1, 2] * 0


@cython.test_assert_path_exists(
    "//BoolNode",
)
@cython.test_fail_if_path_exists(
    "//PrimaryCmpNode",
    "//MulNode",
    "//ListNode//IntNode",
)
def combined():
    """
    >>> combined()
    True
    """
    return 5 in 100 * [1, 2] * 0  or  5 not in 100 * [] * 10


@cython.test_assert_path_exists(
    '//IntNode[@value = "2"]',
    '//IntNode[@value = "4"]',
    '//IntNode[@value = "5"]',
    '//IntNode[@value = "7"]',
    '//BoolBinopNode//PrimaryCmpNode',
    '//BoolBinopNode[.//PrimaryCmpNode//IntNode[@value = "4"] and .//PrimaryCmpNode//IntNode[@value = "5"]]',
    '//PrimaryCmpNode[.//IntNode[@value = "2"] and .//IntNode[@value = "4"]]',
    '//PrimaryCmpNode[.//IntNode[@value = "5"] and .//IntNode[@value = "7"]]',
)
@cython.test_fail_if_path_exists(
    '//IntNode[@value = "1"]',
    '//IntNode[@value = "8"]',
    '//PrimaryCmpNode[.//IntNode[@value = "4"] and .//IntNode[@value = "5"]]',
    '//PrimaryCmpNode[.//IntNode[@value = "2"] and .//IntNode[@value = "7"]]',
    '//BoolNode',
)
def cascaded_cmp_with_partial_constants(a, b):
    """
    >>> cascaded_cmp_with_partial_constants(3, 6)
    True
    >>> cascaded_cmp_with_partial_constants(1, 6)
    False
    >>> cascaded_cmp_with_partial_constants(4, 6)
    False
    >>> cascaded_cmp_with_partial_constants(3, 7)
    False
    >>> cascaded_cmp_with_partial_constants(3, 6)
    True
    """
    return 1 < 2 < a < 4 < 5 < b < 7 < 8


@cython.test_assert_path_exists(
    '//IntNode[@value = "2"]',
    '//IntNode[@value = "4"]',
    '//IntNode[@value = "5"]',
    '//IntNode[@value = "7"]',
    '//BoolBinopNode',
    '//SingleAssignmentNode//BoolBinopNode',
    '//SingleAssignmentNode//BoolBinopNode//NameNode[@name = "a"]',
    '//SingleAssignmentNode//BoolBinopNode//NameNode[@name = "b"]',
    '//BoolBinopNode[.//PrimaryCmpNode//IntNode[@value = "4"] and .//PrimaryCmpNode//IntNode[@value = "5"]]',
    '//BoolNode[@value = False]',
)
@cython.test_fail_if_path_exists(
    '//SingleAssignmentNode//NameNode[@name = "c"]',
    '//IntNode[@value = "1"]',
    '//PrimaryCmpNode[.//IntNode[@value = "4"] and .//IntNode[@value = "5"]]',
    '//PrimaryCmpNode[.//IntNode[@value = "2"] and .//IntNode[@value = "7"]]',
    '//BoolNode[@value = True]',
)
def cascaded_cmp_with_partial_constants_and_false_end(a, b, c):
    """
    >>> cascaded_cmp_with_partial_constants_and_false_end(3, 6, 8)
    False
    >>> cascaded_cmp_with_partial_constants_and_false_end(1, 6, 8)
    False
    >>> cascaded_cmp_with_partial_constants_and_false_end(4, 6, 8)
    False
    >>> cascaded_cmp_with_partial_constants_and_false_end(3, 7, 8)
    False
    """
    x = 1 < 2 < a < 4 < 5 < b < 7 < 7 < c
    return x


@cython.test_assert_path_exists(
    '//PrimaryCmpNode',
    '//PrimaryCmpNode//IntNode',
    '//PrimaryCmpNode//IntNode[@value = "0"]',
    '//PrimaryCmpNode//IntNode[@value = "4294967296"]',
)
@cython.test_fail_if_path_exists(
    '//PrimaryCmpNode//IntBinopNode',
    '//PrimaryCmpNode//IntNode[@value = "1"]',
    '//PrimaryCmpNode//IntNode[@value = "32"]',
)
def const_in_binop(v):
    """
    >>> const_in_binop(-1)
    1
    >>> const_in_binop(0)
    0
    >>> const_in_binop(1 << 32)
    1
    >>> const_in_binop(1 << 32 - 1)
    0
    """
    if v < 0 or v >= (1 << 32):
        return 1
    else:
        return 0
