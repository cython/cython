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
