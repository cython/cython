# mode: run
# tag: cpp, cpp11

# cython: test_assert_c_code_has = call_with_explicit_param\<int\>\(__
# cython: test_fail_if_c_code_has = call_with_implicit_param\<int\>\(__
# cython: test_assert_c_code_has = call_with_implicit_param\(__
# cython: test_assert_c_code_has = call_with_mixed_params\<int\>\(__
# cython: test_assert_c_code_has = can_still_call_explicitly\<double\>\(__

cimport cython

cdef extern from *:
    """
    #include <type_traits>

    template <typename T>
    T call_with_explicit_param(T x) {
        return x;
    }

    template <typename T>
    T call_with_implicit_param(T x) {
        return x;
    }

    template <typename T, typename U>
    T call_with_mixed_params(T x, U y) {
        return x + y;
    }

    template <typename T>
    T can_still_call_explicitly(T x) {
        return x;
    }

    // cases designed not to compile in C++ with an explicit template parameter
    #define call_with_implicit_param_macro(x) x
    template <typename Dummy=double, typename T=double>
    T lie_to_cython_about_parameters(T x) {
        static_assert(!std::is_same<Dummy, int>::value);
        return x;
    }
    """
    T call_with_explicit_param[T](T x)
    T call_with_implicit_param[cython.implicit_param[T]](T x)
    T call_with_mixed_params[T, cython.implicit_param[U]](T x, U y)
    T can_still_call_explicitly[cython.implicit_param[T]](T x)
    T call_with_implicit_param_macro[cython.implicit_param[T]](T x)
    T lie_to_cython_about_parameters[cython.implicit_param[T]](T x)

def do_calls():
    """
    >>> do_calls()
    """
    cdef int x = 1
    cdef long y = 2
    assert call_with_explicit_param(x) == 1
    assert call_with_implicit_param(x) == 1
    assert call_with_mixed_params(x, y) == 3
    assert can_still_call_explicitly[double](x)
    # Code generation not tested for the line below because it'll fail naturally if wrong
    assert call_with_implicit_param_macro(x) == 1
    assert lie_to_cython_about_parameters(x) == 1
