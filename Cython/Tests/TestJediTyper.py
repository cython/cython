# -*- coding: utf-8 -*-
# tag: jedi

from __future__ import absolute_import

import sys
import os.path

from textwrap import dedent
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

from Cython.Compiler.ParseTreeTransforms import NormalizeTree, InterpretCompilerDirectives
from Cython.Compiler import Main, Symtab, Visitor
from Cython.TestUtils import TransformTest

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Tools'))


@contextmanager
def _tempfile(code):
    code = dedent(code)
    if isinstance(code, unicode):
        code = code.encode('utf8')

    with NamedTemporaryFile(suffix='.py') as f:
        f.write(code)
        f.seek(0)
        yield f


def _test_typing(code, inject=False):
    sys.path.insert(0, TOOLS_DIR)
    try:
        module = __import__('jedi-typer')
    finally:
        sys.path.remove(TOOLS_DIR)
    lines = []
    with _tempfile(code) as f:
        types = module.analyse(f.name)
        if inject:
            lines = module.inject_types(f.name, types)
    return types, lines


class DeclarationsFinder(Visitor.VisitorTransform):
    directives = None

    visit_Node = Visitor.VisitorTransform.recurse_to_children

    def visit_CompilerDirectivesNode(self, node):
        if not self.directives:
            self.directives = []
        self.directives.append(node)
        self.visitchildren(node)
        return node


class TestJediTyper(TransformTest):
    def _test(self, code):
        return _test_typing(code)[0]

    def test_typing_global_int_loop(self):
        code = '''\
        for i in range(10):
            a = i + 1
        '''
        types = self._test(code)
        if not types:
            # old Jedi version
            return
        self.assertIn((None, (1, 0)), types)
        variables = types.pop((None, (1, 0)))
        self.assertFalse(types)
        self.assertEqual({'a': set(['int']), 'i': set(['int'])}, variables)

    def test_typing_function_int_loop(self):
        code = '''\
        def func(x):
            for i in range(x):
                a = i + 1
            return a
        '''
        types = self._test(code)
        self.assertIn(('func', (1, 0)), types)
        variables = types.pop(('func', (1, 0)))
        self.assertFalse(types)
        self.assertEqual({'a': set(['int']), 'i': set(['int'])}, variables)

    def _test_conflicting_types_in_function(self):
        code = '''\
        def func(a, b):
            print(a)
            a = 1
            b += a
            a = 'abc'
            return a, str(b)

        print(func(1.5, 2))
        '''
        types = self._test(code)
        self.assertIn(('func', (1, 0)), types)
        variables = types.pop(('func', (1, 0)))
        self.assertFalse(types)
        self.assertEqual({'a': set(['int', 'str']), 'i': set(['int'])}, variables)

    def _test_typing_function_char_loop(self):
        code = '''\
        def func(x):
            l = []
            for c in x:
                l.append(c)
            return l

        print(func('abcdefg'))
        '''
        types = self._test(code)
        self.assertIn(('func', (1, 0)), types)
        variables = types.pop(('func', (1, 0)))
        self.assertFalse(types)
        self.assertEqual({'a': set(['int']), 'i': set(['int'])}, variables)


class TestTypeInjection(TestJediTyper):
    """
    Subtype of TestJediTyper that additionally tests type injection and compilation.
    """
    def setUp(self):
        super(TestTypeInjection, self).setUp()
        compilation_options = Main.CompilationOptions(Main.default_options)
        ctx = compilation_options.create_context()
        transform = InterpretCompilerDirectives(ctx, ctx.compiler_directives)
        transform.module_scope = Symtab.ModuleScope('__main__', None, ctx)
        self.declarations_finder = DeclarationsFinder()
        self.pipeline = [NormalizeTree(None), transform, self.declarations_finder]

    def _test(self, code):
        types, lines = _test_typing(code, inject=True)
        tree = self.run_pipeline(self.pipeline, ''.join(lines))
        directives = self.declarations_finder.directives
        # TODO: validate directives
        return types
