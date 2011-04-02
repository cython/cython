# mode: error

cimport cython

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//NameNode")
@cython.test_assert_path_exists("//ComprehensionNode",
                                "//ComprehensionNode//FuncDefNode")
def test():
    object()


_ERRORS = u"""
9:0: Expected path '//ComprehensionNode' not found in result tree
9:0: Expected path '//ComprehensionNode//FuncDefNode' not found in result tree
9:0: Unexpected path '//NameNode' found in result tree
9:0: Unexpected path '//SimpleCallNode' found in result tree
"""
