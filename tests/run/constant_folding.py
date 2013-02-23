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
    (1.0, -1.0, 1.0, -1.0, -1.0)
    """
    plus1  = + 1.0
    minus1 = - 1.0
    plus3  = +++ 1.0
    minus3 = --- 1.0
    mix    = +-++-- 1.0
    return plus1, minus1, plus3, minus3, mix


@cython.test_fail_if_path_exists(
    "//UnaryMinusNode",
    "//UnaryPlusNode",
)
def unop_ints():
    """
    >>> unop_ints()
    (1, -1, 1, -1, -1)
    """
    plus1  = + 1
    minus1 = - 1
    plus3  = +++ 1
    minus3 = --- 1
    mix    = +-++-- 1
    return plus1, minus1, plus3, minus3, mix
