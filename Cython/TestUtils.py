import Cython.Compiler.Errors as Errors
from Cython.CodeWriter import CodeWriter
import unittest
from Cython.Compiler.ModuleNode import ModuleNode
import Cython.Compiler.Main as Main
from Cython.Compiler.TreeFragment import TreeFragment, strip_common_indent

class CythonTest(unittest.TestCase):
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

