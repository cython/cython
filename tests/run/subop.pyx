cimport cython


def bigint(x):
    print(str(x).rstrip('L'))


def mixed_test():
    """
    >>> mixed_test()
    (-1, -1)
    """
    cdef int int1, int2, int3
    obj1 = 1
    obj2 = 2
    obj3 = 3
    int2 = 2
    int3 = 3

    int1 = int2 - int3
    obj1 = obj2 - int3
    return int1, obj1


def pointer_test():
    """
    >>> pointer_test()
    0
    """
    cdef int int1, int2, int3
    cdef char *ptr1, *ptr2, *ptr3
    int2 = 2
    int3 = 3
    ptr2 = "test"
    ptr3 = ptr2

    ptr1 = ptr2 - int3
    int1 = ptr2 - ptr3
    return int1


@cython.test_fail_if_path_exists('//SubNode')
def sub_x_1(x):
    """
    >>> sub_x_1(0)
    -1
    >>> sub_x_1(1)
    0
    >>> sub_x_1(-1)
    -2
    >>> bigint(2**50 - 1)
    1125899906842623
    >>> bigint(sub_x_1(2**50))
    1125899906842623
    >>> sub_x_1(1.5)
    0.5
    >>> sub_x_1(-1.5)
    -2.5
    >>> try: sub_x_1("abc")
    ... except TypeError: pass
    """
    return x - 1


@cython.test_fail_if_path_exists('//SubNode')
def sub_x_1f(x):
    """
    >>> sub_x_1f(0)
    -1.0
    >>> sub_x_1f(1)
    0.0
    >>> sub_x_1f(-1)
    -2.0
    >>> 2**52 - 1.0
    4503599627370495.0
    >>> sub_x_1f(2**52)
    4503599627370495.0
    >>> sub_x_1f(2**60) == 2**60 - 1.0 or sub_x_1f(2**60)
    True
    >>> sub_x_1f(1.5)
    0.5
    >>> sub_x_1f(-1.5)
    -2.5
    >>> try: sub_x_1f("abc")
    ... except TypeError: pass
    """
    return x - 1.0


@cython.test_fail_if_path_exists('//SubNode')
def sub_x_large(x):
    """
    >>> sub_x_large(0)
    -1073741824
    >>> sub_x_large(1)
    -1073741823
    >>> sub_x_large(-1)
    -1073741825
    >>> bigint(2**50 - 2**30)
    1125898833100800
    >>> bigint(sub_x_large(2**50))
    1125898833100800
    >>> sub_x_large(2.0**30)
    0.0
    >>> sub_x_large(2.0**30 + 1)
    1.0
    >>> sub_x_large(2.0**30 - 1)
    -1.0
    >>> 2.0 ** 31 - 2**30
    1073741824.0
    >>> sub_x_large(2.0**31)
    1073741824.0
    >>> try: sub_x_large("abc")
    ... except TypeError: pass
    """
    return x - 2**30


@cython.test_fail_if_path_exists('//SubNode')
def sub_1_x(x):
    """
    >>> sub_1_x(0)
    1
    >>> sub_1_x(-1)
    2
    >>> sub_1_x(1)
    0
    >>> bigint(1 - 2**50)
    -1125899906842623
    >>> bigint(sub_1_x(2**50))
    -1125899906842623
    >>> sub_1_x(1.5)
    -0.5
    >>> sub_1_x(-1.5)
    2.5
    >>> try: sub_1_x("abc")
    ... except TypeError: pass
    """
    return 1 - x


@cython.test_fail_if_path_exists('//SubNode')
def sub_1f_x(x):
    """
    >>> sub_1f_x(0)
    1.0
    >>> sub_1f_x(-1)
    2.0
    >>> sub_1f_x(1)
    0.0
    >>> 1.0 - 2**52
    -4503599627370495.0
    >>> sub_1f_x(2**52)
    -4503599627370495.0
    >>> sub_1f_x(2**60) == 1.0 - 2**60 or sub_1f_x(2**60)
    True
    >>> sub_1f_x(1.5)
    -0.5
    >>> sub_1f_x(-1.5)
    2.5
    >>> try: sub_1f_x("abc")
    ... except TypeError: pass
    """
    return 1.0 - x


@cython.test_fail_if_path_exists('//SubNode')
def sub_large_x(x):
    """
    >>> sub_large_x(0)
    1073741824
    >>> sub_large_x(-1)
    1073741825
    >>> sub_large_x(1)
    1073741823
    >>> sub_large_x(2**30)
    0
    >>> bigint(2**30 - 2**31)
    -1073741824
    >>> bigint(sub_large_x(2**31))
    -1073741824
    >>> sub_large_x(2.0**30)
    0.0
    >>> sub_large_x(2.0**31)
    -1073741824.0
    >>> sub_large_x(2.0**30 + 1)
    -1.0
    >>> sub_large_x(2.0**30 - 1)
    1.0
    >>> try: sub_large_x("abc")
    ... except TypeError: pass
    """
    return 2**30 - x


def sub0(x):
    """
    >>> sub0(0)
    (0, 0)
    >>> sub0(1)
    (1, -1)
    >>> sub0(-1)
    (-1, 1)
    >>> sub0(99)
    (99, -99)
    >>> a, b = sub0(2**32)
    >>> bigint(a)
    4294967296
    >>> bigint(b)
    -4294967296
    >>> a, b = sub0(-2**32)
    >>> bigint(a)
    -4294967296
    >>> bigint(b)
    4294967296
    """
    return x - 0, 0 - x
