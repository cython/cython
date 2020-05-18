# mode: compile

# This is a sort of meta test - to test the functionality of "test_assert_path_exists"

cimport cython

@cython.test_assert_path_exists("//ReturnStatNode")
def not_in_inner_compiler_directives():
    # used to fail because ReturnStatNode wasn't in *this* CompilerDirectivesNode
    with cython.boundscheck(False):
        pass
    return 1 # should pass

@cython.test_assert_path_exists("//ReturnStatNode")
def in_inner_compiler_directives():
    # used to fail because ReturnStatNode wasn't in *this* CompilerDirectivesNode
    with cython.boundscheck(False):
        return 1

# it's hard to come up with a corresponding test for fail_if_path_exists..
