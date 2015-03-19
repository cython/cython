cimport cython


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
    >>> sub_x_1(1.5)
    0.5
    >>> sub_x_1(-1.5)
    -2.5
    >>> try: sub_x_1("abc")
    ... except TypeError: pass
    """
    return x - 1


@cython.test_fail_if_path_exists('//SubNode')
def sub_x_large(x):
    """
    >>> sub_x_large(0)
    -1073741824
    >>> sub_x_large(1)
    -1073741823
    >>> sub_x_large(-1)
    -1073741825
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
    >>> sub_1_x(1.5)
    -0.5
    >>> sub_1_x(-1.5)
    2.5
    >>> try: sub_1_x("abc")
    ... except TypeError: pass
    """
    return 1 - x


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
    >>> 2**30 - 2**31
    -1073741824
    >>> sub_large_x(2**31)
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
