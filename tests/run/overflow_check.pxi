cimport cython

cdef object two = 2
cdef int size_in_bits = sizeof(INT) * 8

cdef bint is_signed_ = not ((<INT>-1) > 0)
cdef INT max_value_ = <INT>(two ** (size_in_bits - is_signed_) - 1)
cdef INT min_value_ = ~max_value_
cdef INT half_ = max_value_ // <INT>2

# Python visible.
is_signed = is_signed_
max_value = max_value_
min_value = min_value_
half = half_


import operator
from libc.math cimport sqrt

cpdef check(func, op, a, b):
    cdef INT res = 0, op_res = 0
    cdef bint func_overflow = False
    cdef bint assign_overflow = False
    try:
        res = func(a, b)
    except OverflowError:
        func_overflow = True
    try:
        op_res = op(a, b)
    except OverflowError:
        assign_overflow = True
    assert func_overflow == assign_overflow, "Inconsistent overflow: %s(%s, %s)" % (func, a, b)
    if not func_overflow:
        assert res == op_res, "Inconsistent values: %s(%s, %s) == %s != %s" % (func, a, b, res, op_res)

medium_values = (max_value_ / 2, max_value_ / 3, min_value_ / 2, <INT>sqrt(<long double>max_value_) - <INT>1, <INT>sqrt(<long double>max_value_) + 1)
def run_test(func, op):
    cdef INT offset, b
    check(func, op, 300, 200)
    check(func, op, max_value_, max_value_)
    check(func, op, max_value_, min_value_)
    if not is_signed_ or not func is test_sub:
        check(func, op, min_value_, min_value_)

    for offset in range(5):
        check(func, op, max_value_ - <INT>1, offset)
        check(func, op, min_value_ + <INT>1, offset)
        if is_signed_:
            check(func, op, max_value_ - 1, 2 - offset)
            check(func, op, min_value_ + 1, 2 - offset)

    for offset in range(9):
        check(func, op, max_value_ / <INT>2, offset)
        check(func, op, min_value_ / <INT>3, offset)
        check(func, op, max_value_ / <INT>4, offset)
        check(func, op, min_value_ / <INT>5, offset)
        if is_signed_:
            check(func, op, max_value_ / 2, 4 - offset)
            check(func, op, min_value_ / 3, 4 - offset)
            check(func, op, max_value_ / -4, 3 - offset)
            check(func, op, min_value_ / -5, 3 - offset)

    for offset in range(-3, 4):
        for a in medium_values:
            for b in medium_values:
                check(func, op, a, b + offset)

@cython.overflowcheck(True)
def test_add(INT a, INT b):
    """
    >>> test_add(1, 2)
    3
    >>> test_add(max_value, max_value)   #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: value too large
    >>> run_test(test_add, operator.add)
    """
    return int(a + b)
    
@cython.overflowcheck(True)
def test_sub(INT a, INT b):
    """
    >>> test_sub(10, 1)
    9
    >>> test_sub(min_value, 1)   #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: value too large
    >>> run_test(test_sub, operator.sub)
    """
    return int(a - b)

@cython.overflowcheck(True)
def test_mul(INT a, INT b):
    """
    >>> test_mul(11, 13)
    143
    >>> test_mul(max_value / 2, max_value / 2)   #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: value too large
    >>> run_test(test_mul, operator.mul)
    """
    return int(a * b)

@cython.overflowcheck(True)
def test_nested_add(INT a, INT b, INT c):
    """
    >>> test_nested_add(1, 2, 3)
    6
    >>> expect_overflow(test_nested_add, half + 1, half + 1, half + 1)
    >>> expect_overflow(test_nested_add, half - 1, half - 1, half - 1)
    """
    return int(a + b + c)

def expect_overflow(func, *args):
    try:
        res = func(*args)
    except OverflowError:
        return
    assert False, "Expected OverflowError, got %s" % res

cpdef format(INT value):
    """
    >>> format(1)
    '1'
    >>> format(half - 1)
    'half - 1'
    >>> format(half)
    'half'
    >>> format(half + 2)
    'half + 2'
    >>> format(half + half - 3)
    'half + half - 3'
    >>> format(max_value)
    'max_value'
    """
    if value == max_value_:
        return "max_value"
    elif value == half_:
        return "half"
    elif max_value_ - value <= max_value_ // <INT>4:
        return "half + half - %s" % (half_ + half_ - value)
    elif max_value_ - value <= half_:
        return "half + %s" % (value - half_)
    elif max_value_ - value <= half_ + max_value_ // <INT>4:
        return "half - %s" % (half_ - value)
    else:
        return "%s" % value

cdef INT called(INT value):
    print("called(%s)" % format(value))
    return value

@cython.overflowcheck(True)
def test_nested(INT a, INT b, INT c, INT d):
    """
    >>> test_nested_func(1, 2, 3)
    called(5)
    6
    >>> expect_overflow(test_nested, half, half, 1, 1)
    >>> expect_overflow(test_nested, half, 1, half, half)
    >>> expect_overflow(test_nested, half, 2, half, 2)

    >>> print(format(test_nested(half, 2, 0, 1)))
    half + half - 0
    >>> print(format(test_nested(1, 0, half, 2)))
    half + half - 0
    >>> print(format(test_nested(half, 1, 1, half)))
    half + half - 0
    """
    return int(a * b + c * d)

@cython.overflowcheck(True)
def test_nested_func(INT a, INT b, INT c):
    """
    >>> test_nested_func(1, 2, 3)
    called(5)
    6
    >>> expect_overflow(test_nested_func, half + 1, half + 1, half + 1)
    >>> expect_overflow(test_nested_func, half - 1, half - 1, half - 1)
    called(half + half - 2)
    >>> print(format(test_nested_func(1, half - 1, half - 1)))
    called(half + half - 2)
    half + half - 1
    """
    return int(a + called(b + c))


@cython.overflowcheck(True)
def test_add_const(INT a):
    """
    >>> test_add_const(1)
    101
    >>> expect_overflow(test_add_const, max_value)
    >>> expect_overflow(test_add_const , max_value - 99)
    >>> test_add_const(max_value - 100) == max_value
    True
    """
    return int(a + <INT>100)

@cython.overflowcheck(True)
def test_sub_const(INT a):
    """
    >>> test_sub_const(101)
    1
    >>> expect_overflow(test_sub_const, min_value)
    >>> expect_overflow(test_sub_const, min_value + 99)
    >>> test_sub_const(min_value + 100) == min_value
    True
    """
    return int(a - <INT>100)

@cython.overflowcheck(True)
def test_mul_const(INT a):
    """
    >>> test_mul_const(2)
    200
    >>> expect_overflow(test_mul_const, max_value)
    >>> expect_overflow(test_mul_const, max_value // 99)
    >>> test_mul_const(max_value // 100) == max_value - max_value % 100
    True
    """
    return int(a * <INT>100)

@cython.overflowcheck(True)
def test_lshift(INT a, int b):
    """
    >>> test_lshift(1, 10)
    1024
    >>> expect_overflow(test_lshift, 1, 100)
    >>> expect_overflow(test_lshift, max_value, 1)
    >>> test_lshift(max_value, 0) == max_value
    True
    
    >>> check(test_lshift, operator.lshift, 10, 15)
    >>> check(test_lshift, operator.lshift, 10, 30)
    >>> check(test_lshift, operator.lshift, 100, 60)
    """
    return int(a << b)
