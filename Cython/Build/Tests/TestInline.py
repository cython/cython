from Cython.Shadow import inline
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

    def test_simple(self):
        self.assertEquals(inline("return 1+2", **test_kwds), 3)

    def test_types(self):
        self.assertEquals(inline("""
            cimport cython
            return cython.typeof(a), cython.typeof(b)
        """, a=1.0, b=[], **test_kwds), ('double', 'list object'))

    def test_locals(self):
        a = 1
        b = 2
        self.assertEquals(inline("return a+b", **test_kwds), 3)

    def test_globals(self):
        self.assertEquals(inline("return global_value + 1", **test_kwds), global_value + 1)

    if has_numpy:

        def test_numpy(self):
            import numpy
            a = numpy.ndarray((10, 20))
            a[0,0] = 10
            self.assertEquals(safe_type(a), 'numpy.ndarray[numpy.float64_t, ndim=2]')
            self.assertEquals(inline("return a[0,0]", a=a, **test_kwds), 10.0)
