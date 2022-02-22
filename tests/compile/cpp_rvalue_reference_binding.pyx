# tag: cpp, cpp11
# mode: compile

cdef extern from *:
    """
    template <typename T>
    void accept(T&& x) { (void) x; }
    """
    cdef void accept[T](T&& x)

cdef int make_int_py() except *:
    # might raise Python exception (thus needs a temp)
    return 1

cdef int make_int_cpp() except +:
    # might raise C++ exception (thus needs a temp)
    return 1

def test_func_arg():
    # won't compile if move() isn't called on the temp:
    accept(make_int_py())
    accept(make_int_cpp())
