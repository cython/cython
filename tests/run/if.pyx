import cython

def f(a, b):
    """
    >>> f(0,0)
    0
    >>> f(1,2)
    2
    >>> f(1,-1)
    1
    """
    x = 0
    if a:
        x = 1
    if a+b:
        x = 2
    return x

def g(a, b):
    """
    >>> g(1,2)
    1
    >>> g(0,2)
    2
    >>> g(0,0)
    0
    """
    x = 0
    if a:
        x = 1
    elif b:
        x = 2
    return x

def h(a, b):
    """
    >>> h(1,2)
    1
    >>> h(0,2)
    2
    >>> h(0,0)
    3
    """
    x = 0
    if a:
        x = 1
    elif b:
        x = 2
    else:
        x = 3
    return x

try:
    import __builtin__  as builtins
except ImportError:
    import builtins

def i(a, b):
    """
    >>> i(1,2)
    1
    >>> i(2,2)
    2
    >>> i(2,1)
    0
    """
    x = 0
    if builtins.str(a).upper() == u"1":
        x = 1
    if builtins.str(a+b).lower() not in (u"1", u"3"):
        x = 2
    return x


@cython.test_assert_path_exists(
    '//IfClauseNode',
    '//IfClauseNode//BranchHintNode',
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
    '//IfClauseNode',
    '//IfClauseNode//BranchHintNode',
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
    '//IfClauseNode',
    '//IfClauseNode//BranchHintNode',
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
    '//IfClauseNode',
    '//IfClauseNode//BranchHintNode',
)
def branch_hint_exception(int a, int b):
    """
    >>> branch_hint_exception(5, 5)   # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> branch_hint_exception(3, 5)
    'not raised'
    """
    if a == b:
        raise ValueError()
    return 'not raised'

@cython.test_assert_path_exists(
    '//IfClauseNode',
    '//IfClauseNode//BranchHintNode',
)
def branch_hint_else_exception(int a, int b):
    """
    >>> branch_hint_else_exception(5, 5)
    'not raised'
    >>> branch_hint_else_exception(3, 5)   # doctest:+IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    """
    if a == b:
        return 'not raised'
    else:
        raise ValueError()

@cython.test_assert_path_exists(
    '//IfClauseNode',
    '//IfClauseNode//BranchHintNode',
)
def branch_hint_comprehension_cmp(int a, int b):
    """
    >>> branch_hint_comprehension_cmp(5, 3)
    [3]
    """
    return [i for i in range(a) if cython.unlikely(b == i)]
