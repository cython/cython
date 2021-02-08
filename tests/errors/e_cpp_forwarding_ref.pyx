# mode: error
# tag: cpp, cpp11

cdef extern from *:
    """
    #include <utility>

    const char* one_arg(int x) {
        return "first";
    }

    template <typename T>
    const char* one_arg(T&& x)  {
        return one_arg(std::forward<T>(x));
    }
    """
    cdef const char* one_arg[T](T&&)


def test_too_few_arguments():
    cdef const char* result = one_arg()

def test_too_many_arguments():
    cdef const char* result = one_arg(1, 2)

_ERRORS="""
21:37: Call with wrong number of arguments (expected 1, got 0)
24:37: Call with wrong number of arguments (expected 1, got 2)
"""
