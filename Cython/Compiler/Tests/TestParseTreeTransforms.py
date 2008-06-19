from Cython.TestUtils import TransformTest
from Cython.Compiler.ParseTreeTransforms import *
from Cython.Compiler.Nodes import *

class TestPostParse(TransformTest):
    def test_parserbehaviour_is_what_we_coded_for(self):
        t = self.fragment(u"if x: y").root
        self.assertLines(u"""
(root): StatListNode
  stats[0]: IfStatNode
    if_clauses[0]: IfClauseNode
      condition: NameNode
      body: ExprStatNode
        expr: NameNode
""", self.treetypes(t))
        
    def test_wrap_singlestat(self):
    	t = self.run_pipeline([PostParse()], u"if x: y")
        self.assertLines(u"""
(root): StatListNode
  stats[0]: IfStatNode
    if_clauses[0]: IfClauseNode
      condition: NameNode
      body: StatListNode
        stats[0]: ExprStatNode
          expr: NameNode
""", self.treetypes(t))

    def test_wrap_multistat(self):
        t = self.run_pipeline([PostParse()], u"""
            if z:
                x
                y
        """)
        self.assertLines(u"""
(root): StatListNode
  stats[0]: IfStatNode
    if_clauses[0]: IfClauseNode
      condition: NameNode
      body: StatListNode
        stats[0]: ExprStatNode
          expr: NameNode
        stats[1]: ExprStatNode
          expr: NameNode
""", self.treetypes(t))

    def test_statinexpr(self):
        t = self.run_pipeline([PostParse()], u"""
            a, b = x, y
        """)
        self.assertLines(u"""
(root): StatListNode
  stats[0]: ParallelAssignmentNode
    stats[0]: SingleAssignmentNode
      lhs: NameNode
      rhs: NameNode
    stats[1]: SingleAssignmentNode
      lhs: NameNode
      rhs: NameNode
""", self.treetypes(t))

    def test_wrap_offagain(self):
        t = self.run_pipeline([PostParse()], u"""
            x
            y
            if z:
                x
        """)
        self.assertLines(u"""
(root): StatListNode
  stats[0]: ExprStatNode
    expr: NameNode
  stats[1]: ExprStatNode
    expr: NameNode
  stats[2]: IfStatNode
    if_clauses[0]: IfClauseNode
      condition: NameNode
      body: StatListNode
        stats[0]: ExprStatNode
          expr: NameNode
""", self.treetypes(t))
        

    def test_pass_eliminated(self):
        t = self.run_pipeline([PostParse()], u"pass")
        self.assert_(len(t.stats) == 0)

class TestWithTransform(TransformTest):

    def test_simplified(self):
        t = self.run_pipeline([WithTransform()], u"""
        with x:
            y = z ** 3
        """)
        
        self.assertCode(u"""

        $MGR = x
        $EXIT = $MGR.__exit__
        $MGR.__enter__()
        $EXC = True
        try:
            try:
                y = z ** 3
            except:
                $EXC = False
                if (not $EXIT($EXCINFO)):
                    raise
        finally:
            if $EXC:
                $EXIT(None, None, None)

        """, t)

    def test_basic(self):
        t = self.run_pipeline([WithTransform()], u"""
        with x as y:
            y = z ** 3
        """)
        self.assertCode(u"""

        $MGR = x
        $EXIT = $MGR.__exit__
        $VALUE = $MGR.__enter__()
        $EXC = True
        try:
            try:
                y = $VALUE
                y = z ** 3
            except:
                $EXC = False
                if (not $EXIT($EXCINFO)):
                    raise
        finally:
            if $EXC:
                $EXIT(None, None, None)

        """, t)
                          

if __name__ == "__main__":
    import unittest
    unittest.main()
