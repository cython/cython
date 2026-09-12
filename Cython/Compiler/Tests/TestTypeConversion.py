from Cython.Compiler import Code
from Cython.TestUtils import TimedTest


def _function_body(source, signature):
    start = source.index(signature)
    end = source.index("\n}", start)
    return source[start:end]


class TestPyIndexAsSsize_t(TimedTest):
    """
    GH-7979: __Pyx_PyIndex_AsSsize_t lost its compact-int fast path in 3.3.0.
    """

    def test_compact_int_fast_path_present(self):
        proto, impl = Code.TempitaUtilityCode.load_as_string(
            "TypeConversions", "TypeConversion.c")
        source = (proto or "") + (impl or "")
        body = _function_body(source, "__Pyx_PyIndex_AsSsize_t(PyObject* b) {")

        self.assertIn(
            "__Pyx_PyLong_CompactValue", body,
            "missing compact-int fast path (GH-7979): %s" % body)
        self.assertIn(
            "PyLong_CheckExact", body,
            "missing exact-type check before PyLong_Check() (GH-7979): %s" % body)
