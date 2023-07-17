# mode: run
# tag: list, mulop, pure3.0

import cython


@cython.test_fail_if_path_exists("//MulNode")
@cython.test_assert_path_exists("//ListNode[@mult_factor]")
def cint_times_list(n: cython.int):
    """
    >>> cint_times_list(3)
    []
    [None, None, None]
    [3, 3, 3]
    [1, 2, 3, 1, 2, 3, 1, 2, 3]
    """
    a = n * []
    b = n * [None]
    c = n * [n]
    d = n * [1, 2, 3]

    print(a)
    print(b)
    print(c)
    print(d)


@cython.test_fail_if_path_exists("//MulNode")
@cython.test_assert_path_exists("//ListNode[@mult_factor]")
def list_times_cint(n: cython.int):
    """
    >>> list_times_cint(3)
    []
    [None, None, None]
    [3, 3, 3]
    [1, 2, 3, 1, 2, 3, 1, 2, 3]
    """
    a = [] * n
    b = [None] * n
    c = [n] * n
    d = [1, 2, 3] * n

    print(a)
    print(b)
    print(c)
    print(d)


@cython.test_fail_if_path_exists("//MulNode")
@cython.test_assert_path_exists("//TupleNode[@mult_factor]")
def const_times_tuple(v: cython.int):
    """
    >>> const_times_tuple(4)
    ()
    (None, None)
    (4, 4)
    (1, 2, 3, 1, 2, 3)
    """
    a = 2 * ()
    b = 2 * (None,)
    c = 2 * (v,)
    d = 2 * (1, 2, 3)

    print(a)
    print(b)
    print(c)
    print(d)


@cython.test_fail_if_path_exists("//MulNode")
@cython.test_assert_path_exists("//TupleNode[@mult_factor]")
def cint_times_tuple(n: cython.int):
    """
    >>> cint_times_tuple(3)
    ()
    (None, None, None)
    (3, 3, 3)
    (1, 2, 3, 1, 2, 3, 1, 2, 3)
    """
    a = n * ()
    b = n * (None,)
    c = n * (n,)
    d = n * (1, 2, 3)

    print(a)
    print(b)
    print(c)
    print(d)


@cython.test_fail_if_path_exists("//MulNode")
@cython.test_assert_path_exists("//TupleNode[@mult_factor]")
def tuple_times_cint(n: cython.int):
    """
    >>> tuple_times_cint(3)
    ()
    (None, None, None)
    (3, 3, 3)
    (1, 2, 3, 1, 2, 3, 1, 2, 3)
    """
    a = () * n
    b = (None,) * n
    c = (n,) * n
    d = (1, 2, 3) * n

    print(a)
    print(b)
    print(c)
    print(d)


# TODO: enable in Cython 3.1 when we can infer unsafe C int operations as PyLong
#@cython.test_fail_if_path_exists("//MulNode")
def list_times_pyint(n: cython.longlong):
    """
    >>> list_times_cint(3)
    []
    [None, None, None]
    [3, 3, 3]
    [1, 2, 3, 1, 2, 3, 1, 2, 3]
    """
    py_n = n + 1  # might overflow => should be inferred as Python long!

    a = [] * py_n
    b = [None] * py_n
    c = py_n * [n]
    d = py_n * [1, 2, 3]

    print(a)
    print(b)
    print(c)
    print(d)


@cython.cfunc
def sideeffect(x) -> cython.int:
    global _sideeffect_value
    _sideeffect_value += 1
    return _sideeffect_value + x


def reset_sideeffect():
    global _sideeffect_value
    _sideeffect_value = 0


@cython.test_fail_if_path_exists("//MulNode")
@cython.test_assert_path_exists("//ListNode[@mult_factor]")
def complicated_cint_times_list(n: cython.int):
    """
    >>> complicated_cint_times_list(3)
    []
    [None, None, None, None]
    [3, 3, 3, 3]
    [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    """
    reset_sideeffect()
    a = [] * sideeffect((lambda: n)())
    reset_sideeffect()
    b = sideeffect((lambda: n)()) * [None]
    reset_sideeffect()
    c = [n] * sideeffect((lambda: n)())
    reset_sideeffect()
    d = sideeffect((lambda: n)()) * [1, 2, 3]

    print(a)
    print(b)
    print(c)
    print(d)
