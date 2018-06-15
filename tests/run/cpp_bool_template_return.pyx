# tag: cpp

from libcpp cimport bool

cdef extern from "cpp_templates_helper.h":
    cdef cppclass BinaryAnd[T1, T2]:
        @staticmethod
        T1 call(T1 x, T2 y)


def test_compound_bool_return(bool x, bool y):
    """
    >>> test_compound_bool_return(True, False)
    False
    """
    return BinaryAnd[bool, bool].call(x, y)
