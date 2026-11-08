# mode: error
# tag: cpp

cimport cython
import some_module

cdef extern from *:
    void f[cython.implicit_param[T], U](T x, U y)
    void g[cython.hopefully_this_will_never_become_an_allowed_thing_to_put_in_a_template[T]](T x)
    # Not cimported
    void h[implicit_param[T]](T x)
    void i[some_module.implicit_param[T]](T x)

_ERRORS = """
8:37: Non-implicit template argument follows implicit template argument
9:88: Only 'implicit_param' is accepted as an indexed template argument
9:93: 'T' is not a type identifier
11:25: Only 'implicit_param' is accepted as an indexed template argument
11:30: 'T' is not a type identifier
12:37: Only 'implicit_param' is accepted as an indexed template argument
12:42: 'T' is not a type identifier
"""
