from Cython.TestUtils import TransformTest
from Cython.Compiler.ParseTreeTransforms import *
from Cython.Compiler.Nodes import *

class TestNormalizeTree(TransformTest):
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
        t = self.run_pipeline([NormalizeTree(None)], u"if x: y")
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
        t = self.run_pipeline([NormalizeTree(None)], u"""
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
        t = self.run_pipeline([NormalizeTree(None)], u"""
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
        t = self.run_pipeline([NormalizeTree(None)], u"""
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
        t = self.run_pipeline([NormalizeTree(None)], u"pass")
        self.assert_(len(t.stats) == 0)

class TestWithTransform(object): # (TransformTest): # Disabled!

    def test_simplified(self):
        t = self.run_pipeline([WithTransform(None)], u"""
        with x:
            y = z ** 3
        """)

        self.assertCode(u"""

        $0_0 = x
        $0_2 = $0_0.__exit__
        $0_0.__enter__()
        $0_1 = True
        try:
            try:
                $1_0 = None
                y = z ** 3
            except:
                $0_1 = False
                if (not $0_2($1_0)):
                    raise
        finally:
            if $0_1:
                $0_2(None, None, None)

        """, t)

    def test_basic(self):
        t = self.run_pipeline([WithTransform(None)], u"""
        with x as y:
            y = z ** 3
        """)
        self.assertCode(u"""

        $0_0 = x
        $0_2 = $0_0.__exit__
        $0_3 = $0_0.__enter__()
        $0_1 = True
        try:
            try:
                $1_0 = None
                y = $0_3
                y = z ** 3
            except:
                $0_1 = False
                if (not $0_2($1_0)):
                    raise
        finally:
            if $0_1:
                $0_2(None, None, None)

        """, t)
                          

if __name__ == "__main__":
    import unittest
    unittest.main()
