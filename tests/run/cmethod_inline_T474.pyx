# mode: run
# ticket: t474
cimport cython


cdef class TestInlineMethod(object):
    """
    >>> test = TestInlineMethod()
    >>> test.test_cdef_method()
    0
    """

    @cython.test_assert_path_exists(
        "//AttributeNode[@entry.is_inline_cmethod=True]",
        "//AttributeNode[@entry.is_final_cmethod=True]")
    def test_cdef_method(self):
        return self.cdef_inline_method()


cdef class Subtyping(TestInlineMethod):
    """
    >>> test = Subtyping()
    >>> test.test_cdef_subtyping()
    0
    """

    @cython.test_assert_path_exists(
        "//AttributeNode[@entry.is_inline_cmethod=True]",
        "//AttributeNode[@entry.is_final_cmethod=True]")
    def test_cdef_subtyping(self):
        return self.cdef_inline_method()
