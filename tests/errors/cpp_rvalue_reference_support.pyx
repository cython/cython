# mode: error
# tag: werror, cpp, cpp11

# These tests check for unsupported use of rvalue-references (&&)
# and should be removed or cleaned up when support is added.

cdef i32&& x

cdef void foo(i32&& x):
    pass

cdef i32&& bar():
    pass

cdef extern from *:
    """
    void baz(int x, int&& y) {}

    template <typename T>
    void qux(const T&& x) {}
    """
    cdef void baz(i32 x, i32&& y)
    cdef void qux[T](const T&& x)


_ERRORS="""
7:8: C++ rvalue-references cannot be declared
9:13: Rvalue-reference as function argument not supported
12:14: Rvalue-reference as function return type not supported
22:17: Rvalue-reference as function argument not supported
23:20: Rvalue-reference as function argument not supported
"""
