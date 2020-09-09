# mode: run
# tag: cpp, cpp11

from libcpp.utility cimport move


cdef extern from *:
    """
    #include <utility>

    const char* f(int& x) {
        return "lvalue-ref";
    }

    const char* f(int&& x) {
        return "rvalue-ref";
    }
    
    template <typename T>
    const char* foo(T&& x)
    {
        return f(std::forward<T>(x));
    }
    """
    const char* foo[T](T&& x)


def test_forwarding_basic():
    cdef int x = 1
    assert foo(x) == b"lvalue-ref"
    assert foo(move(x)) == b"rvalue-ref"

