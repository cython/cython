# mode: run
# tag: cpp, cpp11, no-cpp-locals

from libcpp.utility cimport move


cdef extern from *:
    """
    #include <utility>

    const char* f(int& x) {
        (void) x;
        return "lvalue-ref";
    }

    const char* f(int&& x) {
        (void) x;
        return "rvalue-ref";
    }

    template <typename T>
    const char* foo(T&& x)
    {
        return f(std::forward<T>(x));
    }
    """
    const char* foo[T](T&& x)


cdef extern from *:
    """
    #include <utility>

    template <typename T1>
    const char* bar(T1 x, T1 y) {
        return "first";
    }

    template <typename T1, typename T2>
    const char* bar(T1&& x, T2 y, T2 z) {
        return "second";
    }

    """
    const char* bar[T1](T1 x, T1 y)
    const char* bar[T1, T2](T1&& x, T2 y, T2 z)

def test_forwarding_ref():
    """
    >>> test_forwarding_ref()
    """
    cdef int x = 1
    assert foo(x) == b"lvalue-ref"
    assert foo(<int>(1)) == b"rvalue-ref"
    assert foo(move(x)) == b"rvalue-ref"


def test_forwarding_ref_overload():
    """
    >>> test_forwarding_ref_overload()
    """
    cdef int x = 1
    cdef int y = 2
    cdef int z = 3
    assert bar(x, y) == b"first"
    assert bar(x, y, z) == b"second"
