import unittest
from Cython.TestUtils import TransformTest
from Cython.Compiler.ParseTreeTransforms import DecoratorTransform

class TestDecorator(TransformTest):

    def test_decorator(self):
        t = self.run_pipeline([DecoratorTransform(None)], u"""
        def decorator(fun):
            return fun
        @decorator
        def decorated():
            pass
        """)

        self.assertCode(u"""
        def decorator(fun):
            return fun
        def decorated():
            pass
        decorated = decorator(decorated)
        """, t)

if __name__ == '__main__':
    unittest.main()
