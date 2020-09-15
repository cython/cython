# mode: error
# tag: cpp11

# These test check for unsupported use of rvalue-references (&&)
# and should be when support is added.

cdef int&& x

cdef void foo(int&& x):
    pass

cdef int&& bar():
    pass

cdef extern from *:
    """
    void baz(int x, int&& y) {}

    template <typename T>
    void qux(const T&& x) {}
    """
    cdef void baz(int x, int&& y)
    cdef void qux[T](const T&& x)


_ERRORS="""
4:8: C++ rvalue-references cannot be declared
6:13: Rvalue-reference as function argument not supported
9:14: Rvalue-reference as function return type not supported
19:17: Rvalue-reference as function argument not supported
20:20: Rvalue-reference as function argument not supported
"""
