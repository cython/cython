# mode: compile
# tag: if, unlikely

cimport cython


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[not(@branch_hint)]",
)
def if_simple(x):
    if x:
        x = 2


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[not(@branch_hint)]",
)
def if_return(x):
    if x:
        return 1
    raise TypeError()


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'unlikely']",
)
def if_raise_else(x):
    if x:
        raise TypeError()
    else:
        return 1


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'likely']",
)
def if_else_raise(x):
    if x:
        return 1
    else:
        raise TypeError()


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'unlikely']",
)
def if_raise_else_raise(x):
    if x:
        raise ValueError()
    else:
        raise TypeError()


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'unlikely']",
)
@cython.test_fail_if_path_exists(
    "//IfClauseNode[@branch_hint = 'likely']",
    "//IfClauseNode[not(@branch_hint)]",
)
def if_elif_raise_else_raise(x):
    if x:
        raise ValueError()
    elif not x:
        raise AttributeError()
    else:
        raise TypeError()


@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'unlikely']",
    "//IfClauseNode[@branch_hint = 'unlikely']//GILStatNode",
)
@cython.test_fail_if_path_exists(
    "//IfClauseNode[@branch_hint = 'likely']",
    "//IfClauseNode[not(@branch_hint)]",
)
cpdef int nogil_if_raise(int x) except -1 nogil:
    if x:
        raise TypeError()
    elif not x:
        raise ValueError()
    else:
        x = 2

@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'likely']",
)
def branch_hint_likely(int a, int b):
    """
    >>> branch_hint_likely(5, 3)
    'a > b'
    >>> branch_hint_likely(3, 5)
    'a < b'
    """
    if cython.likely(a > b):
        return "a > b"
    return "a < b"

@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'unlikely']",
)
def branch_hint_unlikely(int a, int b):
    """
    >>> branch_hint_unlikely(5, 5)
    'a == b'
    >>> branch_hint_unlikely(3, 5)
    'a != b'
    """
    if cython.unlikely(a == b):
        return "a == b"
    return "a != b"

@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'likely']",
)
def branch_hint_likely_exception(int a, int b):
    # Cython automatically injects `unlikely()` in
    # if conditions having branch with single raise line.
    # This tests verifies that Cython correctly injects likely()
    """
    >>> branch_hint_likely_exception(5, 5)   # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> branch_hint_likely_exception(3, 5)
    'not raised'
    """
    if cython.likely(a == b):
        raise ValueError()
    return 'not raised'

@cython.test_assert_path_exists(
    "//IfClauseNode",
    "//IfClauseNode[@branch_hint = 'unlikely']",
)
def branch_hint_comprehension_cmp(int a, int b):
    """
    >>> branch_hint_comprehension_cmp(5, 3)
    [3]
    """
    return [i for i in range(a) if cython.unlikely(b == i)]
