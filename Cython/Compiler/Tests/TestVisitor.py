from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Symtab import ModuleScope
from Cython.TestUtils import TransformTest, TimedTest
from Cython.Compiler.Visitor import MethodDispatcherTransform, _test_flatten_list as test_flatten_list
from Cython.Compiler.ParseTreeTransforms import (
    NormalizeTree, AnalyseDeclarationsTransform,
    AnalyseExpressionsTransform, InterpretCompilerDirectives)


class TestMethodDispatcherTransform(TransformTest):
    _tree = None

    def _build_tree(self):
        if self._tree is None:
            context = None

            def fake_module(node):
                scope = ModuleScope('test', None, None)
                return ModuleNode(node.pos, doc=None, body=node,
                                  scope=scope, full_module_name='test',
                                  directive_comments={})
            pipeline = [
                fake_module,
                NormalizeTree(context),
                InterpretCompilerDirectives(context, {}),
                AnalyseDeclarationsTransform(context),
                AnalyseExpressionsTransform(context),
            ]
            self._tree = self.run_pipeline(pipeline, """
                cdef bytes s = b'asdfg'
                cdef dict d = {1:2}
                x = s * 3
                d.get('test')
            """)
        return self._tree

    def test_builtin_method(self):
        calls = [0]
        class Test(MethodDispatcherTransform):
            def _handle_simple_method_dict_get(self, node, func, args, unbound):
                calls[0] += 1
                return node

        tree = self._build_tree()
        Test(None)(tree)
        self.assertEqual(1, calls[0])

    def test_binop_method(self):
        calls = {'bytes': 0, 'object': 0}
        class Test(MethodDispatcherTransform):
            def _handle_simple_method_bytes___mul__(self, node, func, args, unbound):
                calls['bytes'] += 1
                return node
            def _handle_simple_method_object___mul__(self, node, func, args, unbound):
                calls['object'] += 1
                return node

        tree = self._build_tree()
        Test(None)(tree)
        self.assertEqual(1, calls['bytes'])
        self.assertEqual(0, calls['object'])


class TestVisitorTransform(TimedTest):
    def test_flatten_list_unchanged(self):
        for test_list in [[], [1], [1,2], [0], [0,0]]:
            self.assertIs(test_flatten_list(test_list), test_list)

    def test_flatten_list_unchanged_sublist(self):
        for test_list in [
                [[1]],
                [[1,2]],
                [[1,2], 3],
                [[1,2], None, []],
                ]:
            self.assertIs(test_flatten_list(test_list), test_list[0])

        for test_list in [
                [None, [1]],
                [[], [1,2]],
                [[], [1,2], []],
                [[], [1,2], None],
                [[], [1,2], 3],
                [None, [1,2], None, []],
                [None, [1,2], None, [3]],
                ]:
            self.assertIs(test_flatten_list(test_list), test_list[1])

    def test_flatten_list_mixed(self):
        self.assertListEqual(test_flatten_list([1, []]), [1])
        self.assertListEqual(test_flatten_list([[], [], []]), [])
        self.assertListEqual(test_flatten_list([[], None, []]), [])
        self.assertListEqual(test_flatten_list([None, [], None]), [])
        self.assertListEqual(test_flatten_list([1, [2]]), [1, 2])
        self.assertListEqual(test_flatten_list([[1], [2]]), [1, 2])
        self.assertListEqual(test_flatten_list([[1,2], [3,4]]), [1, 2, 3, 4])
        self.assertListEqual(test_flatten_list([[1,2], [0], [], 0, [4]]), [1, 2, 0, 0, 4])

    def test_flatten_list_fuzzer(self):
        def flatten(l):
            return [
                item
                for item_or_list in filter(None, l)
                for item in (item_or_list if type(item_or_list) is list else [item_or_list])
            ]

        from itertools import chain, combinations as mixer
        test_items = [None, [], None, 1, [2], [], 3, None, [4], [5, 6], [], None]

        from collections import defaultdict
        counter = defaultdict(int)

        for test_list in chain.from_iterable(mixer(test_items, length) for length in range(2, 7)):
            counter[len(test_list)] += 1
            test_list = list(test_list)
            expected = flatten(test_list)
            self.assertListEqual(test_flatten_list(test_list), expected)

        #print("FUZZER TEST COUNTS:", dict(counter))
