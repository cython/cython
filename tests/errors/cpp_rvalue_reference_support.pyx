# mode: error
# tag: werror, cpp, cpp11

# These tests check for unsupported use of rvalue-references (&&)
# and should be removed or cleaned up when support is added.

cdef i32&& x

fn void foo(i32&& x):
    pass

fn i32&& bar():
    pass

extern from *:
    """
    void baz(int x, int&& y) {}

    template <typename T>
    void qux(const T&& x) {}
    """
    fn void baz(i32 x, i32&& y)
    fn void qux[T](const T&& x)


_ERRORS="""
7:8: C++ rvalue-references cannot be declared
9:11: Rvalue-reference as function argument not supported
12:12: Rvalue-reference as function return type not supported
22:15: Rvalue-reference as function argument not supported
23:18: Rvalue-reference as function argument not supported
"""
