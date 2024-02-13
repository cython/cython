# mode: error
# tag: werror

cdef object test_return_object_noexcept(x) noexcept:
    return x

cdef str test_return_str_noexcept() noexcept:
    return 'a'

cdef test_noexcept() noexcept:
    pass

cdef extern from *:
    cdef object extern_return_object():
        pass

    cdef object extern_noexcept() noexcept:
        pass

ctypedef fused double_or_object:
    double
    object

cdef double_or_object test_fused_noexcept(double_or_object x) noexcept:
    pass

_ERRORS = """
4:39: noexcept clause is ignored for function returning Python object
7:33: noexcept clause is ignored for function returning Python object
10:18: noexcept clause is ignored for function returning Python object
"""
