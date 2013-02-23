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
