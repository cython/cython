# mode: error
# tag: cpp, werror

from libcpp.set cimport set

cdef extern from *:
    void cpp_function_set1(set[int] arg)
    void cpp_function_set2(set[int]& arg)


def pass_py_obj_as_cpp_cont_ref():
    cdef list ordered_set = [0, 0, 0, 0, 0]
    cpp_function_set1(ordered_set)
    cpp_function_set2(ordered_set)


_ERRORS = """
14:22: Cannot pass Python object as C++ data structure reference (set[int] &), will pass by copy.
"""
