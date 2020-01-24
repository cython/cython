import os, tempfile
from types import ModuleType
from Cython.Shadow import inline, inline_module
from Cython.Build.Inline import safe_type
from Cython.TestUtils import CythonTest

try:
    import numpy
    has_numpy = True
except:
    has_numpy = False

test_kwds = dict(force=True, quiet=True)

global_value = 100

class TestInline(CythonTest):
    def setUp(self):
        CythonTest.setUp(self)
        self.test_kwds = dict(test_kwds)
        if os.path.isdir('TEST_TMP'):
            lib_dir = os.path.join('TEST_TMP', 'inline')
        else:
            lib_dir = tempfile.mkdtemp(prefix='cython_inline_')
        self.test_kwds['lib_dir'] = lib_dir

    def test_simple(self):
        self.assertEqual(inline("return 1+2", **self.test_kwds), 3)

    def test_types(self):
        self.assertEqual(inline("""
            cimport cython
            return cython.typeof(a), cython.typeof(b)
        """, a=1.0, b=[], **self.test_kwds), ('double', 'list object'))

    def test_locals(self):
        a = 1
        b = 2
        self.assertEqual(inline("return a+b", **self.test_kwds), 3)

    def test_globals(self):
        self.assertEqual(inline("return global_value + 1", **self.test_kwds), global_value + 1)

    def test_no_return(self):
        self.assertEqual(inline("""
            a = 1
            cdef double b = 2
            cdef c = []
        """, **self.test_kwds), dict(a=1, b=2.0, c=[]))

    def test_def_node(self):
        foo = inline("def foo(x): return x * x", **self.test_kwds)['foo']
        self.assertEqual(foo(7), 49)

    def test_class_ref(self):
        class Type(object):
            pass
        tp = inline("Type")['Type']
        self.assertEqual(tp, Type)

    def test_pure(self):
        import cython as cy
        b = inline("""
        b = cy.declare(float, a)
        c = cy.declare(cy.pointer(cy.float), &b)
        return b
        """, a=3, **self.test_kwds)
        self.assertEqual(type(b), float)

    def test_compiler_directives(self):
        self.assertEqual(
            inline('return sum(x)',
                   x=[1, 2, 3],
                   cython_compiler_directives={'boundscheck': False}),
            6
        )

    if has_numpy:
        def test_numpy(self):
            import numpy
            a = numpy.ndarray((10, 20))
            a[0, 0] = 10
            self.assertEqual(safe_type(a), 'numpy.ndarray[numpy.float64_t, ndim=2]')
            self.assertEqual(inline("return a[0,0]", a=a, **self.test_kwds), 10.0)


class TestInlineModule(CythonTest):
    def setUp(self):
        CythonTest.setUp(self)
        self.test_kwds = dict(test_kwds)
        if os.path.isdir('TEST_TMP'):
            module_cache_dir = os.path.join('TEST_TMP', 'inline')
        else:
            module_cache_dir = tempfile.mkdtemp(prefix='cython_inline_module_')
        self.test_kwds['module_cache_dir'] = module_cache_dir

    def test_simple(self):
        module = inline_module("""
            def test_fn():
                return 1+2
            """,
            **self.test_kwds)
        self.assertEqual(module.test_fn(), 3)
        self.assertEqual(type(module), ModuleType)

    def test_caching(self):
        module1 = inline_module("""
            def test_fn():
                return 1+2
            """,
            **self.test_kwds)
        module2 = inline_module("""
            def test_fn():
                return 1+2
            """,
            **self.test_kwds)
        self.assertIs(module1, module2)

    def test_indent_stripping_with_zero_indent_string(self):
        module = inline_module("""
            def test_fn():
                test_string = '''
This is a test string.
                '''
                return 1+2
            """,
            **self.test_kwds)
        self.assertEqual(module.test_fn(), 3)
        self.assertEqual(type(module), ModuleType)

    def test_cdef_node(self):
        module = inline_module(
            """
            from libc.stdint cimport uintptr_t

            cdef foo(x):
                return x * x

            foo_ptr = <uintptr_t>&foo
            """,
            **self.test_kwds)
        self.assertNotEqual(module.foo_ptr, 0)
        self.assertEqual(type(module.foo_ptr), int)
