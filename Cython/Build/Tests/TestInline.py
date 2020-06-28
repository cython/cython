import os
import sys
import tempfile
import textwrap
import unittest
from Cython.Shadow import inline, compile as cython_compile, boundscheck
from Cython.Build.Inline import safe_type
from Cython.TestUtils import CythonTest

try:
    import numpy
    has_numpy = True
except:
    has_numpy = False

test_kwds = dict(force=True, quiet=True)

global_value = 100

class CythonInlineTest(CythonTest):
    def setUp(self):
        super(CythonInlineTest, self).setUp()
        self.test_kwds = dict(test_kwds)
        if os.path.isdir('TEST_TMP'):
            lib_dir = os.path.join('TEST_TMP','inline')
        else:
            lib_dir = tempfile.mkdtemp(prefix='cython_inline_')
        self.test_kwds['lib_dir'] = lib_dir


class TestInline(CythonInlineTest):
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

    def test_lang_version(self):
        # GH-3419. Caching for inline code didn't always respect compiler directives.
        inline_divcode = "def f(int a, int b): return a/b"
        self.assertEqual(
            inline(inline_divcode, language_level=2)['f'](5,2),
            2
        )
        self.assertEqual(
            inline(inline_divcode, language_level=3)['f'](5,2),
            2.5
        )
        self.assertEqual(
            inline(inline_divcode, language_level=2)['f'](5,2),
            2
        )

    def test_repeated_use(self):
        inline_mulcode = "def f(int a, int b): return a * b"
        self.assertEqual(inline(inline_mulcode)['f'](5, 2), 10)
        self.assertEqual(inline(inline_mulcode)['f'](5, 3), 15)
        self.assertEqual(inline(inline_mulcode)['f'](6, 2), 12)
        self.assertEqual(inline(inline_mulcode)['f'](5, 2), 10)

        f = inline(inline_mulcode)['f']
        self.assertEqual(f(5, 2), 10)
        self.assertEqual(f(5, 3), 15)

    @unittest.skipIf(not has_numpy, "NumPy is not available")
    def test_numpy(self):
        import numpy
        a = numpy.ndarray((10, 20))
        a[0,0] = 10
        self.assertEqual(safe_type(a), 'numpy.ndarray[numpy.float64_t, ndim=2]')
        self.assertEqual(inline("return a[0,0]", a=a, **self.test_kwds), 10.0)


class TestCompileDecorator(CythonInlineTest):
    def test_no_kwargs(self):
        old_cache_dir = os.environ.get('CYTHON_CACHE_DIR', '')
        os.environ['CYTHON_CACHE_DIR'] = self.test_kwds['lib_dir']
        try:
            # We need to make sure that compilation works when there are no
            # arguments to the decorator
            @cython_compile
            def test_fn(x):
                return x + 1
        finally:
            os.environ['CYTHON_CACHE_DIR'] = old_cache_dir

        self.assertEqual(test_fn(1), 2)

    def test_kwargs(self):

        @cython_compile(**self.test_kwds)
        def test_fn(x=":"):
            return x + 1

        self.assertEqual(test_fn(1), 2)

    def test_no_decorator(self):

        def test_fn(x):
            return x + 1

        # The decorator should work as a normal function, too
        test_fn = cython_compile(**self.test_kwds)(test_fn)

        self.assertEqual(test_fn(1), 2)

        # It should also work when there's another decorator
        @boundscheck(False)
        def test_fn(x):
            return x + 1

        test_fn = cython_compile(**self.test_kwds)(test_fn)

        self.assertEqual(test_fn(1), 2)

    @unittest.skipIf(not has_numpy, "NumPy is not available")
    def test_numpy(self):

        import numpy as np

        # Make sure the aliased module dependency is handled properly
        @cython_compile(**self.test_kwds)
        def test_fn(x):
            return np.add(x, 1)

        self.assertEqual(test_fn(1), 2)

    @unittest.skipIf(sys.version_info < (3, 6), "Requires Py3.6+")
    def test_type_hints(self):
        fd, tmp_code_file = tempfile.mkstemp(suffix='.py', text=True)
        with os.fdopen(fd, 'w') as f:
            tmp_code = textwrap.dedent("""
            def test_fn(x: int, y: float) -> int:
                b: int = 1
                return x + int(y) + b
            """)
            f.write(tmp_code)

        locals = {}
        exec(compile(tmp_code, tmp_code_file, 'exec'), None, locals)

        assert 'test_fn' in locals
        test_fn = locals['test_fn']

        test_fn = cython_compile(**self.test_kwds)(test_fn)

        self.assertEqual(test_fn(1, 2), 4)

    def test_decorator_with_decorator(self):

        @cython_compile(**self.test_kwds)
        @boundscheck(False)
        def test_fn(x):
            return x[0]

        self.assertEqual(test_fn([0]), 0)
