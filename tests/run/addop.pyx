cimport cython


def mixed_test():
    """
    >>> mixed_test()
    (30, 22)
    """
    cdef int int1, int2, int3
    cdef char *ptr1, *ptr2 = "test", *ptr3 = "toast"
    int2 = 10
    int3 = 20
    obj1 = 1
    obj2 = 2
    obj3 = 3
    int1 = int2 + int3
    ptr1 = ptr2 + int3
    ptr1 = int2 + ptr3
    obj1 = obj2 + int3
    return int1, obj1


@cython.test_fail_if_path_exists('//AddNode')
def add_x_1(x):
    """
    >>> add_x_1(0)
    1
    >>> add_x_1(1)
    2
    >>> add_x_1(-1)
    0
    >>> add_x_1(1.5)
    2.5
    >>> add_x_1(-1.5)
    -0.5
    >>> try: add_x_1("abc")
    ... except TypeError: pass
    """
    return x + 1


@cython.test_fail_if_path_exists('//AddNode')
def add_x_large(x):
    """
    >>> add_x_large(0)
    1073741824
    >>> add_x_large(1)
    1073741825
    >>> add_x_large(-1)
    1073741823
    >>> add_x_large(1.5)
    1073741825.5
    >>> add_x_large(-2.0**31)
    -1073741824.0
    >>> add_x_large(2**30 + 1)
    2147483649
    >>> 2**31 + 2**30
    3221225472
    >>> add_x_large(2**31)
    3221225472
    >>> print(2**66 + 2**30)
    73786976295911948288
    >>> print(add_x_large(2**66))
    73786976295911948288
    >>> try: add_x_large("abc")
    ... except TypeError: pass
    """
    return x + 2**30


@cython.test_fail_if_path_exists('//AddNode')
def add_1_x(x):
    """
    >>> add_1_x(0)
    1
    >>> add_1_x(1)
    2
    >>> add_1_x(-1)
    0
    >>> add_1_x(1.5)
    2.5
    >>> add_1_x(-1.5)
    -0.5
    >>> try: add_1_x("abc")
    ... except TypeError: pass
    """
    return 1 + x


@cython.test_fail_if_path_exists('//AddNode')
def add_large_x(x):
    """
    >>> add_large_x(0)
    1073741824
    >>> add_large_x(1)
    1073741825
    >>> add_large_x(-1)
    1073741823
    >>> add_large_x(1.5)
    1073741825.5
    >>> add_large_x(-2.0**30)
    0.0
    >>> add_large_x(-2.0**31)
    -1073741824.0
    >>> try: add_large_x("abc")
    ... except TypeError: pass
    """
    return 2**30 + x
