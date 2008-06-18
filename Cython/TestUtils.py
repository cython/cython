import Cython.Compiler.Errors as Errors
from Cython.CodeWriter import CodeWriter
import unittest
from Cython.Compiler.ModuleNode import ModuleNode
import Cython.Compiler.Main as Main
from Cython.Compiler.TreeFragment import TreeFragment, strip_common_indent
from Cython.Compiler.Visitor import TreeVisitor

class NodeTypeWriter(TreeVisitor):
    def __init__(self):
        super(NodeTypeWriter, self).__init__()
        self._indents = 0
        self.result = []
    def visit_Node(self, node):
        if len(self.access_path) == 0:
            name = u"(root)"
        else:
            tip = self.access_path[-1]
            if tip[2] is not None:
                name = u"%s[%d]" % tip[1:3]
            else:
                name = tip[1]
            
        self.result.append(u"  " * self._indents +
                           u"%s: %s" % (name, node.__class__.__name__))
        self._indents += 1
        self.visitchildren(node)
        self._indents -= 1

class CythonTest(unittest.TestCase):

    def assertLines(self, expected, result):
        "Checks that the given strings or lists of strings are equal line by line"
        if not isinstance(expected, list): expected = expected.split(u"\n")
        if not isinstance(result, list): result = result.split(u"\n")
        for idx, (expected_line, result_line) in enumerate(zip(expected, result)):
            self.assertEqual(expected_line, result_line, "Line %d:\nExp: %s\nGot: %s" % (idx, expected_line, result_line))
        self.assertEqual(len(expected), len(result),
            "Unmatched lines. Got:\n%s\nExpected:\n%s" % ("\n".join(expected), u"\n".join(result)))

    def assertCode(self, expected, result_tree):
        writer = CodeWriter()
        writer.write(result_tree)
        result_lines = writer.result.lines
                
        expected_lines = strip_common_indent(expected.split("\n"))
        
        for idx, (line, expected_line) in enumerate(zip(result_lines, expected_lines)):
            self.assertEqual(expected_line, line, "Line %d:\nGot: %s\nExp: %s" % (idx, line, expected_line))
        self.assertEqual(len(result_lines), len(expected_lines),
            "Unmatched lines. Got:\n%s\nExpected:\n%s" % ("\n".join(result_lines), expected))

    def fragment(self, code, pxds={}):
        "Simply create a tree fragment using the name of the test-case in parse errors."
        name = self.id()
        if name.startswith("__main__."): name = name[len("__main__."):]
        name = name.replace(".", "_")
        return TreeFragment(code, name, pxds)

    def treetypes(self, root):
        """Returns a string representing the tree by class names.
        There's a leading and trailing whitespace so that it can be
        compared by simple string comparison while still making test
        cases look ok."""
        w = NodeTypeWriter()
        w.visit(root)
        return u"\n".join([u""] + w.result + [u""])

class TransformTest(CythonTest):
    """
    Utility base class for transform unit tests. It is based around constructing
    test trees (either explicitly or by parsing a Cython code string); running
    the transform, serialize it using a customized Cython serializer (with
    special markup for nodes that cannot be represented in Cython),
    and do a string-comparison line-by-line of the result.

    To create a test case:
     - Call run_pipeline. The pipeline should at least contain the transform you
       are testing; pyx should be either a string (passed to the parser to
       create a post-parse tree) or a ModuleNode representing input to pipeline.
       The result will be a transformed result (usually a ModuleNode).
       
     - Check that the tree is correct. If wanted, assertCode can be used, which
       takes a code string as expected, and a ModuleNode in result_tree
       (it serializes the ModuleNode to a string and compares line-by-line).
    
    All code strings are first stripped for whitespace lines and then common
    indentation.
       
    Plans: One could have a pxd dictionary parameter to run_pipeline.
    """

    
    def run_pipeline(self, pipeline, pyx, pxds={}):
        tree = self.fragment(pyx, pxds).root
        assert isinstance(tree, ModuleNode)
        # Run pipeline
        for T in pipeline:
            tree = T(tree)
        return tree    

