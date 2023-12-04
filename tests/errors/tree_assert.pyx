# mode: error

cimport cython

@cython.test_fail_if_path_exists("//SimpleCallNode",
                                 "//NameNode")
@cython.test_assert_path_exists("//ComprehensionNode",
                                "//ComprehensionNode//FuncDefNode")
def test():
    object()


_ERRORS = u"""
5:0: Expected path '//ComprehensionNode' not found in result tree
5:0: Expected path '//ComprehensionNode//FuncDefNode' not found in result tree
10:4: Unexpected path '//NameNode' found in result tree
10:10: Unexpected path '//SimpleCallNode' found in result tree
"""
