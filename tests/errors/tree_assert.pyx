# mode: error

cimport cython

@cython.test_fail_if_path_exists(
    "//PyMethodCallNode",
    "//NameNode",
)
@cython.test_assert_path_exists(
    "//ComprehensionNode",
    "//ComprehensionNode//FuncDefNode",
)
def test():
    object()


_ERRORS = u"""
5:0: Expected path '//ComprehensionNode' not found in result tree
5:0: Expected path '//ComprehensionNode//FuncDefNode' not found in result tree
14:4: Unexpected path '//NameNode' found in result tree
14:10: Unexpected path '//PyMethodCallNode' found in result tree
"""
