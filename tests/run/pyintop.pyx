# cython: language_level=3str
# mode: run

cimport cython

from operator import lshift as py_lshift, rshift as py_rshift


def bigint(x):
    # avoid 'L' postfix in Py2.x
    print(str(x).rstrip('L'))

def bigints(x):
    # avoid 'L' postfix in Py2.x
    print(str(x).replace('L', ''))


@cython.test_assert_path_exists('//BitwiseOrNode')
def or_obj(obj2, obj3):
    """
    >>> or_obj(2, 3)
    3
    """
    obj1 = obj2 | obj3
    return obj1


@cython.test_fail_if_path_exists('//BitwiseOrNode')
def or_int(obj2):
    """
    >>> or_int(0)
    16
    >>> or_int(1)
    17
    >>> or_int(16)
    16
    """
    obj1 = obj2 | 0x10
    return obj1


@cython.test_assert_path_exists('//IntBinopNode')
def xor_obj(obj2, obj3):
    """
    >>> xor_obj(2, 3)
    1
    """
    obj1 = obj2 ^ obj3
    return obj1


@cython.test_fail_if_path_exists('//IntBinopNode')
def xor_int(obj2):
    """
    >>> xor_int(0)
    16
    >>> xor_int(2)
    18
    >>> xor_int(16)
    0
    """
    obj1 = obj2 ^ 0x10
    return obj1


@cython.test_assert_path_exists('//IntBinopNode')
def and_obj(obj2, obj3):
    """
    >>> and_obj(2, 3)
    2
    """
    obj1 = obj2 & obj3
    return obj1


@cython.test_fail_if_path_exists('//IntBinopNode')
def and_int(obj2):
    """
    >>> and_int(0)
    0
    >>> and_int(1)
    0
    >>> and_int(18)
    16
    >>> and_int(-1)
    16
    """
    obj1 = obj2 & 0x10
    return obj1


@cython.test_fail_if_path_exists('//IntBinopNode')
def and_int2(obj2):
    # On Python 3.10 and earlier, from_bytes produces a non-canonical
    # 0 that caused trouble when &ing with a constant.
    """
    >>> and_int2(1337)
    57
    >>> and_int2(int.from_bytes(b'\\x00', 'big'))
    0
    """
    obj1 = obj2 & 0xff
    return obj1


@cython.test_assert_path_exists('//IntBinopNode')
def lshift_obj(obj2, obj3):
    """
    >>> lshift_obj(2, 3)
    16
    """
    obj1 = obj2 << obj3
    return obj1


@cython.test_assert_path_exists('//IntBinopNode')
def rshift_obj(obj2, obj3):
    """
    >>> rshift_obj(2, 3)
    0
    """
    obj1 = obj2 >> obj3
    return obj1


@cython.test_assert_path_exists('//IntBinopNode')
def rshift_int_obj(obj3):
    """
    >>> rshift_int_obj(3)
    0
    >>> rshift_int_obj(2)
    0
    >>> rshift_int_obj(1)
    1
    >>> rshift_int_obj(0)
    2
    >>> rshift_int_obj(-1)
    Traceback (most recent call last):
    ValueError: negative shift count
    """
    obj1 = 2 >> obj3
    return obj1


@cython.test_fail_if_path_exists('//IntBinopNode')
def rshift_int(obj2):
    """
    >>> rshift_int(0)
    0
    >>> rshift_int(2)
    0

    >>> rshift_int(27)
    3
    >>> (-27) >> 3
    -4
    >>> rshift_int(-27)
    -4

    >>> rshift_int(32)
    4
    >>> (-32) >> 3
    -4
    >>> rshift_int(-32)
    -4

    >>> (2**28) >> 3
    33554432
    >>> rshift_int(2**28)
    33554432
    >>> (-2**28) >> 3
    -33554432
    >>> rshift_int(-2**28)
    -33554432

    >>> (2**30) >> 3
    134217728
    >>> rshift_int(2**30)
    134217728
    >>> rshift_int(-2**30)
    -134217728

    >>> bigint((2**60) >> 3)
    144115188075855872
    >>> bigint(rshift_int(2**60))
    144115188075855872
    >>> bigint(rshift_int(-2**60))
    -144115188075855872

    >>> rshift_int(-1)
    -1
    >>> (-1) >> 3
    -1
    """
    obj1 = obj2 >> 3
    return obj1


@cython.test_assert_path_exists(
    '//SingleAssignmentNode//IntBinopNode',
    '//SingleAssignmentNode//PythonCapiCallNode',
)
def lshift_int(obj):
    """
    >>> lshift_int(0)
    (0, 0, 0, 0)
    >>> bigints(lshift_int(1))
    (8, 2147483648, 9223372036854775808, 10633823966279326983230456482242756608)
    >>> bigints(lshift_int(-1))
    (-8, -2147483648, -9223372036854775808, -10633823966279326983230456482242756608)
    >>> bigints(lshift_int(2))
    (16, 4294967296, 18446744073709551616, 21267647932558653966460912964485513216)

    >>> bigints(lshift_int(27))
    (216, 57982058496, 249031044995078946816, 287113247089541828547222325020554428416)
    >>> (-27) << 3
    -216
    >>> bigints(lshift_int(-27))
    (-216, -57982058496, -249031044995078946816, -287113247089541828547222325020554428416)

    >>> bigints(lshift_int(32))
    (256, 68719476736, 295147905179352825856, 340282366920938463463374607431768211456)
    >>> (-32) << 3
    -256
    >>> bigints(lshift_int(-32))
    (-256, -68719476736, -295147905179352825856, -340282366920938463463374607431768211456)

    >>> bigint((2**28) << 3)
    2147483648
    >>> bigints(lshift_int(2**28))
    (2147483648, 576460752303423488, 2475880078570760549798248448, 2854495385411919762116571938898990272765493248)
    >>> bigint((-2**28) << 3)
    -2147483648
    >>> bigints(lshift_int(-2**28))
    (-2147483648, -576460752303423488, -2475880078570760549798248448, -2854495385411919762116571938898990272765493248)

    >>> bigint((2**30) << 3)
    8589934592
    >>> bigints(lshift_int(2**30))
    (8589934592, 2305843009213693952, 9903520314283042199192993792, 11417981541647679048466287755595961091061972992)
    >>> bigints(lshift_int(-2**30))
    (-8589934592, -2305843009213693952, -9903520314283042199192993792, -11417981541647679048466287755595961091061972992)

    >>> bigint((2**60) << 3)
    9223372036854775808
    >>> bigints(lshift_int(2**60))
    (9223372036854775808, 2475880078570760549798248448, 10633823966279326983230456482242756608, 12259964326927110866866776217202473468949912977468817408)
    >>> bigints(lshift_int(-2**60))
    (-9223372036854775808, -2475880078570760549798248448, -10633823966279326983230456482242756608, -12259964326927110866866776217202473468949912977468817408)
    """
    r1 = obj << 3
    r2 = obj << 31
    r3 = obj << 63
    r4 = obj << 123
    return r1, r2, r3, r4


@cython.test_assert_path_exists(
    '//IntBinopNode',
    '//BitwiseOrNode//IntBinopNode',
)
def mixed_obj(obj2, obj3):
    """
    >>> mixed_obj(2, 3)
    16
    """
    obj1 = obj2 << obj3 | obj2 >> obj3
    return obj1


@cython.test_assert_path_exists(
    '//BitwiseOrNode',
    '//BitwiseOrNode//PythonCapiCallNode',
)
@cython.test_fail_if_path_exists(
    '//IntBinopNode//IntBinopNode',
)
def mixed_int(obj2):
    """
    >>> mixed_int(0)
    16
    >>> mixed_int(2)
    18
    >>> mixed_int(16)
    0
    >>> mixed_int(17)
    1
    """
    obj1 = (obj2 ^ 0x10) | (obj2 & 0x01)
    return obj1


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//IntBinopNode',
    '//PrimaryCmpNode',
)
def equals(obj2):
    """
    >>> equals(2)
    True
    >>> equals(0)
    False
    >>> equals(-1)
    False
    """
    result = obj2 == 2
    return result


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//IntBinopNode',
    '//PrimaryCmpNode',
)
def not_equals(obj2):
    """
    >>> not_equals(2)
    False
    >>> not_equals(0)
    True
    >>> not_equals(-1)
    True
    """
    result = obj2 != 2
    return result


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_assert_path_exists('//PrimaryCmpNode')
def equals_many(obj2):
    """
    >>> equals_many(-2)
    (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> equals_many(0)
    (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> equals_many(1)
    (False, True, False, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> equals_many(-1)
    (False, False, True, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> equals_many(2**30)
    (False, False, False, True, False, False, False, False, False, False, False, False, False, False, False)
    >>> equals_many(-2**30)
    (False, False, False, False, True, False, False, False, False, False, False, False, False, False, False)
    >>> equals_many(2**30-1)
    (False, False, False, False, False, True, False, False, False, False, False, False, False, False, False)
    >>> equals_many(-2**30+1)
    (False, False, False, False, False, False, True, False, False, False, False, False, False, False, False)
    >>> equals_many(2**32)
    (False, False, False, False, False, False, False, True, False, False, False, False, False, False, False)
    >>> equals_many(-2**32)
    (False, False, False, False, False, False, False, False, True, False, False, False, False, False, False)
    >>> equals_many(2**45-1)
    (False, False, False, False, False, False, False, False, False, True, False, False, False, False, False)
    >>> equals_many(-2**45+1)
    (False, False, False, False, False, False, False, False, False, False, True, False, False, False, False)
    >>> equals_many(2**64)
    (False, False, False, False, False, False, False, False, False, False, False, True, False, False, False)
    >>> equals_many(-2**64)
    (False, False, False, False, False, False, False, False, False, False, False, False, True, False, False)
    >>> equals_many(2**64-1)
    (False, False, False, False, False, False, False, False, False, False, False, False, False, True, False)
    >>> equals_many(-2**64+1)
    (False, False, False, False, False, False, False, False, False, False, False, False, False, False, True)
    """
    cdef bint x, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o
    a = obj2 == 0
    x = 0 == obj2
    assert a == x
    b = obj2 == 1
    x = 1 == obj2
    assert b == x
    c = obj2 == -1
    x = -1 == obj2
    assert c == x
    d = obj2 == 2**30
    x = 2**30 == obj2
    assert d == x
    e = obj2 == -2**30
    x = -2**30 == obj2
    assert e == x
    f = obj2 == 2**30-1
    x = 2**30-1 == obj2
    assert f == x
    g = obj2 == -2**30+1
    x = -2**30+1 == obj2
    assert g == x
    h = obj2 == 2**32
    x = 2**32 == obj2
    assert h == x
    i = obj2 == -2**32
    x = -2**32 == obj2
    assert i == x
    j = obj2 == 2**45-1
    x = 2**45-1 == obj2
    assert j == x
    k = obj2 == -2**45+1
    x = -2**45+1 == obj2
    assert k == x
    l = obj2 == 2**64
    x = 2**64 == obj2
    assert l == x
    m = obj2 == -2**64
    x = -2**64 == obj2
    assert m == x
    n = obj2 == 2**64-1
    x = 2**64-1 == obj2
    assert n == x
    o = obj2 == -2**64+1
    x = -2**64+1 == obj2
    assert o == x
    return (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o)


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_assert_path_exists('//PrimaryCmpNode')
def not_equals_many(obj2):
    """
    >>> not_equals_many(-2)
    (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(0)
    (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(1)
    (False, True, False, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(-1)
    (False, False, True, False, False, False, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(2**30)
    (False, False, False, True, False, False, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(-2**30)
    (False, False, False, False, True, False, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(2**30-1)
    (False, False, False, False, False, True, False, False, False, False, False, False, False, False, False)
    >>> not_equals_many(-2**30+1)
    (False, False, False, False, False, False, True, False, False, False, False, False, False, False, False)
    >>> not_equals_many(2**32)
    (False, False, False, False, False, False, False, True, False, False, False, False, False, False, False)
    >>> not_equals_many(-2**32)
    (False, False, False, False, False, False, False, False, True, False, False, False, False, False, False)
    >>> not_equals_many(2**45-1)
    (False, False, False, False, False, False, False, False, False, True, False, False, False, False, False)
    >>> not_equals_many(-2**45+1)
    (False, False, False, False, False, False, False, False, False, False, True, False, False, False, False)
    >>> not_equals_many(2**64)
    (False, False, False, False, False, False, False, False, False, False, False, True, False, False, False)
    >>> not_equals_many(-2**64)
    (False, False, False, False, False, False, False, False, False, False, False, False, True, False, False)
    >>> not_equals_many(2**64-1)
    (False, False, False, False, False, False, False, False, False, False, False, False, False, True, False)
    >>> not_equals_many(-2**64+1)
    (False, False, False, False, False, False, False, False, False, False, False, False, False, False, True)
    """
    cdef bint a, b, c, d, e, f, g, h, i, j, k, l, m, n, o
    a = obj2 != 0
    x = 0 != obj2
    assert a == x
    b = obj2 != 1
    x = 1 != obj2
    assert b == x
    c = obj2 != -1
    x = -1 != obj2
    assert c == x
    d = obj2 != 2**30
    x = 2**30 != obj2
    assert d == x
    e = obj2 != -2**30
    x = -2**30 != obj2
    assert e == x
    f = obj2 != 2**30-1
    x = 2**30-1 != obj2
    assert f == x
    g = obj2 != -2**30+1
    x = -2**30+1 != obj2
    assert g == x
    h = obj2 != 2**32
    x = 2**32 != obj2
    assert h == x
    i = obj2 != -2**32
    x = -2**32 != obj2
    assert i == x
    j = obj2 != 2**45-1
    x = 2**45-1 != obj2
    assert j == x
    k = obj2 != -2**45+1
    x = -2**45+1 != obj2
    assert k == x
    l = obj2 != 2**64
    x = 2**64 != obj2
    assert l == x
    m = obj2 != -2**64
    x = -2**64 != obj2
    assert m == x
    n = obj2 != 2**64-1
    x = 2**64-1 != obj2
    assert n == x
    o = obj2 != -2**64+1
    x = -2**64+1 != obj2
    assert o == x
    return tuple(not x for x in (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o))


@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists(
    '//IntBinopNode',
    '//PrimaryCmpNode',
)
def equals_zero(obj2):
    """
    >>> equals_zero(2)
    False
    >>> equals_zero(0)
    True
    >>> equals_zero(-1)
    False
    """
    result = obj2 == 0
    return result


def truthy(obj2):
    """
    >>> truthy(2)
    True
    >>> truthy(0)
    False
    >>> truthy(-1)
    True
    """
    if obj2:
        return True
    else:
        return False

@cython.test_fail_if_path_exists("//CoerceToBooleanNode")
@cython.test_fail_if_path_exists("//CoerceToPyTypeNode")
def test_avoid_if_coercion(obj):
    if obj == 1:  # this should not go through a Python intermediate
        return True
    else:
        return False

@cython.test_fail_if_path_exists('//AddNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_add_int(obj2: int):
    """
    >>> pure_add_int(1)
    (2, 2)
    """
    res1 = obj2 + 1
    res2 = 1 + obj2
    return res1, res2

@cython.test_fail_if_path_exists('//SubNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_sub_int(obj2: int):
    """
    >>> pure_sub_int(1)
    (0, 0)
    """
    res1 = obj2 - 1
    res2 = 1 - obj2
    return res1, res2

@cython.test_fail_if_path_exists('//MulNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_mul_int(obj2: int):
    """
    >>> pure_mul_int(2)
    (4, 4)
    """
    res1 = obj2 * 2
    res2 = 2 * obj2
    return res1, res2

@cython.test_fail_if_path_exists('//PrimaryCmpNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_eq_int(obj2: int):
    """
    >>> pure_eq_int(2)
    (True, True)
    >>> pure_eq_int(3)
    (False, False)
    """
    res1 = obj2 == 2
    res2 = 2 == obj2
    return res1, res2

@cython.test_fail_if_path_exists('//PrimaryCmpNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_ne_int(obj2: int):
    """
    >>> pure_ne_int(2)
    (False, False)
    >>> pure_ne_int(3)
    (True, True)
    """
    res1 = obj2 != 2
    res2 = 2 != obj2
    return res1, res2

@cython.test_fail_if_path_exists('//IntBinopNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_and_int(obj2: int):
    """
    >>> pure_and_int(1)
    (0, 0)
    >>> pure_and_int(3)
    (2, 2)
    """
    res1 = obj2 & 2
    res2 = 2 & obj2
    return res1, res2

@cython.test_fail_if_path_exists('//IntBinopNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_or_int(obj2: int):
    """
    >>> pure_or_int(1)
    (3, 3)
    >>> pure_or_int(0)
    (2, 2)
    """
    res1 = obj2 | 2
    res2 = 2 | obj2
    return res1, res2

@cython.test_fail_if_path_exists('//IntBinopNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_xor_int(obj2: int):
    """
    >>> pure_xor_int(1)
    (3, 3)
    >>> pure_xor_int(3)
    (1, 1)
    """
    res1 = obj2 ^ 2
    res2 = 2 ^ obj2
    return res1, res2

@cython.test_fail_if_path_exists('//IntBinopNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_rshift_int(obj2: int):
    """
    >>> pure_rshift_int(8)
    4
    """
    res = obj2 >> 1
    return res

@cython.test_fail_if_path_exists('//IntBinopNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_lshift_int(obj2: int):
    """
    >>> pure_lshift_int(8)
    16
    """
    res = obj2 << 1
    return res

@cython.test_fail_if_path_exists('//IntBinopNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_mod_int(obj2: int):
    """
    >>> pure_mod_int(3)
    1
    """
    res = obj2 % 2
    return res

@cython.test_fail_if_path_exists('//DivNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_floordiv_int(obj2: int):
    """
    >>> pure_floordiv_int(3)
    1
    """
    res = obj2 // 2
    return res

import sys


@cython.test_fail_if_path_exists('//DivNode')
@cython.test_fail_if_path_exists('//NumBinopNode')
@cython.test_fail_if_path_exists('//BinopNode')
@cython.test_assert_path_exists('//PythonCapiFunctionNode')
def pure_truediv_int(obj2: int):
    """
    >>> pure_truediv_int(5)
    2.5
    """
    res = obj2 / 2
    return res


def negative_rhs_lshift(obj: int):
    """
    >>> negative_rhs_lshift(5)
    Traceback (most recent call last):
        ...
    ValueError: negative shift count
    """
    return (obj << (-1))

def negative_rhs_rshift(obj: int):
    """
    >>> negative_rhs_rshift(5)
    Traceback (most recent call last):
        ...
    ValueError: negative shift count
    """
    return (obj >> (-1))


def big_lshift(obj):
    """
    >>> big_lshift(1)
    1180591620717411303424
    >>> big_lshift(-1)
    -1180591620717411303424
    """
    return obj << 70

def somewhat_big_lshift(obj):
    """
    Note that on MSVC this is bigger than a long

    >>> somewhat_big_lshift(1)
    (1099511627776, 4294967296)
    >>> somewhat_big_lshift(-1)
    (-1099511627776, -4294967296)
    """
    return obj << 40, obj << 32

def big_rshift(obj):
    """
    >>> big_rshift(1)
    0
    >>> big_rshift(-1)
    -1
    >>> big_rshift(2**80)
    1024
    >>> big_rshift(-(2**80))
    -1024
    """
    return obj >> 70

def somewhat_big_rshift(obj):
    """
    Note that on MSVC this is bigger than a long

    >>> somewhat_big_rshift(1)
    (0, 0)
    >>> somewhat_big_rshift(-1)
    (-1, -1)
    >>> somewhat_big_rshift(0x6f)
    (0, 0)
    >>> somewhat_big_rshift(-0x6f)
    (-1, -1)
    >>> somewhat_big_rshift(2**50)
    (1024, 262144)
    >>> somewhat_big_rshift(-(2**50))
    (-1024, -262144)
    """
    return obj >> 40, obj >> 32

cdef compare_lshift(obj, shift, cython_result):
    py_result = py_lshift(obj, shift)
    assert cython_result == py_result, f"{obj} << {shift} == {cython_result} != {py_result}"

cdef compare_rshift(obj, shift, cython_result):
    py_result = py_rshift(obj, shift)
    assert cython_result == py_result, f"{obj} >> {shift} == {cython_result} != {py_result}"

cdef compare_both_shifts(obj, shift, cython_lresult, cython_rresult):
    compare_lshift(obj, shift, cython_lresult)
    compare_rshift(obj, shift, cython_rresult)

def integer_shifts(obj):
    """
    >>> integer_shifts(0)
    >>> integer_shifts(1)
    >>> integer_shifts(-1)
    >>> integer_shifts(0xff)
    >>> integer_shifts(-0xff)
    >>> integer_shifts(0xff00)
    >>> integer_shifts(-0xff00)
    >>> integer_shifts(0xff0000)
    >>> integer_shifts(-0xff0000)
    >>> integer_shifts(0xff000000)
    >>> integer_shifts(-0xff000000)
    """
    compare_both_shifts(obj, 0, obj << 0, obj >> 0)
    compare_both_shifts(obj, 1, obj << 1, obj >> 1)
    compare_both_shifts(obj, 2, obj << 2, obj >> 2)
    compare_both_shifts(obj, 3, obj << 3, obj >> 3)
    compare_both_shifts(obj, 4, obj << 4, obj >> 4)
    compare_both_shifts(obj, 5, obj << 5, obj >> 5)
    compare_both_shifts(obj, 6, obj << 6, obj >> 6)
    compare_both_shifts(obj, 7, obj << 7, obj >> 7)
    compare_both_shifts(obj, 8, obj << 8, obj >> 8)
    compare_both_shifts(obj, 9, obj << 9, obj >> 9)
    compare_both_shifts(obj, 10, obj << 10, obj >> 10)
    compare_both_shifts(obj, 11, obj << 11, obj >> 11)
    compare_both_shifts(obj, 12, obj << 12, obj >> 12)
    compare_both_shifts(obj, 13, obj << 13, obj >> 13)
    compare_both_shifts(obj, 14, obj << 14, obj >> 14)
    compare_both_shifts(obj, 15, obj << 15, obj >> 15)
    compare_both_shifts(obj, 16, obj << 16, obj >> 16)
    compare_both_shifts(obj, 17, obj << 17, obj >> 17)
    compare_both_shifts(obj, 18, obj << 18, obj >> 18)
    compare_both_shifts(obj, 19, obj << 19, obj >> 19)
    compare_both_shifts(obj, 20, obj << 20, obj >> 20)
    compare_both_shifts(obj, 21, obj << 21, obj >> 21)
    compare_both_shifts(obj, 22, obj << 22, obj >> 22)
    compare_both_shifts(obj, 23, obj << 23, obj >> 23)
    compare_both_shifts(obj, 24, obj << 24, obj >> 24)
    compare_both_shifts(obj, 25, obj << 25, obj >> 25)
    compare_both_shifts(obj, 26, obj << 26, obj >> 26)
    compare_both_shifts(obj, 27, obj << 27, obj >> 27)
    compare_both_shifts(obj, 28, obj << 28, obj >> 28)
    compare_both_shifts(obj, 29, obj << 29, obj >> 29)
    compare_both_shifts(obj, 30, obj << 30, obj >> 30)
    compare_both_shifts(obj, 31, obj << 31, obj >> 31)
    compare_both_shifts(obj, 32, obj << 32, obj >> 32)
    compare_both_shifts(obj, 33, obj << 33, obj >> 33)
    compare_both_shifts(obj, 34, obj << 34, obj >> 34)
    compare_both_shifts(obj, 35, obj << 35, obj >> 35)
    compare_both_shifts(obj, 36, obj << 36, obj >> 36)
    compare_both_shifts(obj, 37, obj << 37, obj >> 37)
    compare_both_shifts(obj, 38, obj << 38, obj >> 38)
    compare_both_shifts(obj, 39, obj << 39, obj >> 39)
    compare_both_shifts(obj, 40, obj << 40, obj >> 40)
    compare_both_shifts(obj, 41, obj << 41, obj >> 41)
    compare_both_shifts(obj, 42, obj << 42, obj >> 42)
    compare_both_shifts(obj, 43, obj << 43, obj >> 43)
    compare_both_shifts(obj, 44, obj << 44, obj >> 44)
    compare_both_shifts(obj, 45, obj << 45, obj >> 45)
    compare_both_shifts(obj, 46, obj << 46, obj >> 46)
    compare_both_shifts(obj, 47, obj << 47, obj >> 47)
    compare_both_shifts(obj, 48, obj << 48, obj >> 48)
    compare_both_shifts(obj, 49, obj << 49, obj >> 49)
    compare_both_shifts(obj, 50, obj << 50, obj >> 50)
    compare_both_shifts(obj, 51, obj << 51, obj >> 51)
    compare_both_shifts(obj, 52, obj << 52, obj >> 52)
    compare_both_shifts(obj, 53, obj << 53, obj >> 53)
    compare_both_shifts(obj, 54, obj << 54, obj >> 54)
    compare_both_shifts(obj, 55, obj << 55, obj >> 55)
    compare_both_shifts(obj, 56, obj << 56, obj >> 56)
    compare_both_shifts(obj, 57, obj << 57, obj >> 57)
    compare_both_shifts(obj, 58, obj << 58, obj >> 58)
    compare_both_shifts(obj, 59, obj << 59, obj >> 59)
    compare_both_shifts(obj, 60, obj << 60, obj >> 60)
    compare_both_shifts(obj, 61, obj << 61, obj >> 61)
    compare_both_shifts(obj, 62, obj << 62, obj >> 62)
    compare_both_shifts(obj, 63, obj << 63, obj >> 63)
    compare_both_shifts(obj, 64, obj << 64, obj >> 64)
    compare_both_shifts(obj, 65, obj << 65, obj >> 65)
    compare_both_shifts(obj, 66, obj << 66, obj >> 66)
    compare_both_shifts(obj, 67, obj << 67, obj >> 67)
    compare_both_shifts(obj, 68, obj << 68, obj >> 68)
    compare_both_shifts(obj, 69, obj << 69, obj >> 69)
    compare_both_shifts(obj, 70, obj << 70, obj >> 70)
    compare_both_shifts(obj, 71, obj << 71, obj >> 71)
    compare_both_shifts(obj, 72, obj << 72, obj >> 72)
    compare_both_shifts(obj, 73, obj << 73, obj >> 73)
    compare_both_shifts(obj, 74, obj << 74, obj >> 74)
    compare_both_shifts(obj, 75, obj << 75, obj >> 75)
    compare_both_shifts(obj, 76, obj << 76, obj >> 76)
    compare_both_shifts(obj, 77, obj << 77, obj >> 77)
    compare_both_shifts(obj, 78, obj << 78, obj >> 78)
    compare_both_shifts(obj, 79, obj << 79, obj >> 79)
    compare_both_shifts(obj, 80, obj << 80, obj >> 80)
    compare_both_shifts(obj, 81, obj << 81, obj >> 81)
    compare_both_shifts(obj, 82, obj << 82, obj >> 82)
    compare_both_shifts(obj, 83, obj << 83, obj >> 83)
    compare_both_shifts(obj, 84, obj << 84, obj >> 84)
    compare_both_shifts(obj, 85, obj << 85, obj >> 85)
    compare_both_shifts(obj, 86, obj << 86, obj >> 86)
    compare_both_shifts(obj, 87, obj << 87, obj >> 87)
    compare_both_shifts(obj, 88, obj << 88, obj >> 88)
    compare_both_shifts(obj, 89, obj << 89, obj >> 89)
    compare_both_shifts(obj, 90, obj << 90, obj >> 90)
    compare_both_shifts(obj, 91, obj << 91, obj >> 91)
    compare_both_shifts(obj, 92, obj << 92, obj >> 92)
    compare_both_shifts(obj, 93, obj << 93, obj >> 93)
    compare_both_shifts(obj, 94, obj << 94, obj >> 94)
    compare_both_shifts(obj, 95, obj << 95, obj >> 95)
    compare_both_shifts(obj, 96, obj << 96, obj >> 96)
    compare_both_shifts(obj, 97, obj << 97, obj >> 97)
    compare_both_shifts(obj, 98, obj << 98, obj >> 98)
    compare_both_shifts(obj, 99, obj << 99, obj >> 99)
    compare_both_shifts(obj, 100, obj << 100, obj >> 100)
    compare_both_shifts(obj, 101, obj << 101, obj >> 101)
    compare_both_shifts(obj, 102, obj << 102, obj >> 102)
    compare_both_shifts(obj, 103, obj << 103, obj >> 103)
    compare_both_shifts(obj, 104, obj << 104, obj >> 104)
    compare_both_shifts(obj, 105, obj << 105, obj >> 105)
    compare_both_shifts(obj, 106, obj << 106, obj >> 106)
    compare_both_shifts(obj, 107, obj << 107, obj >> 107)
    compare_both_shifts(obj, 108, obj << 108, obj >> 108)
    compare_both_shifts(obj, 109, obj << 109, obj >> 109)
    compare_both_shifts(obj, 110, obj << 110, obj >> 110)
    compare_both_shifts(obj, 111, obj << 111, obj >> 111)
    compare_both_shifts(obj, 112, obj << 112, obj >> 112)
    compare_both_shifts(obj, 113, obj << 113, obj >> 113)
    compare_both_shifts(obj, 114, obj << 114, obj >> 114)
    compare_both_shifts(obj, 115, obj << 115, obj >> 115)
    compare_both_shifts(obj, 116, obj << 116, obj >> 116)
    compare_both_shifts(obj, 117, obj << 117, obj >> 117)
    compare_both_shifts(obj, 118, obj << 118, obj >> 118)
    compare_both_shifts(obj, 119, obj << 119, obj >> 119)
    compare_both_shifts(obj, 120, obj << 120, obj >> 120)
    compare_both_shifts(obj, 121, obj << 121, obj >> 121)
    compare_both_shifts(obj, 122, obj << 122, obj >> 122)
    compare_both_shifts(obj, 123, obj << 123, obj >> 123)
    compare_both_shifts(obj, 124, obj << 124, obj >> 124)
    compare_both_shifts(obj, 125, obj << 125, obj >> 125)
    compare_both_shifts(obj, 126, obj << 126, obj >> 126)
    compare_both_shifts(obj, 127, obj << 127, obj >> 127)
    compare_both_shifts(obj, 128, obj << 128, obj >> 128)
    compare_both_shifts(obj, 129, obj << 129, obj >> 129)
