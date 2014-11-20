# mode: error
# tag: werror

from libcpp.set cimport set

cdef extern from "foo.cpp":
    void cpp_function_set1(set[int])
    void cpp_function_set2(set[int] &)


def pass_py_obj_as_cpp_cont_ref():
    cdef list ordered_set = [0, 0, 0, 0, 0]
    cpp_function_set1(ordered_set)
    cpp_function_set2(ordered_set)


_ERRORS = """
5:13: '<init>' redeclared
5:13: '<init>' redeclared
6:13: '<init>' redeclared
6:13: '<init>' redeclared
6:13: '<init>' redeclared
6:13: '<init>' redeclared
6:13: '<init>' redeclared
7:13: '<init>' redeclared
7:13: '<init>' redeclared
7:13: '<init>' redeclared
14:33: Cannot pass Python object as C++ data structure reference (set[int] &), will pass by copy.
21:12: '<init>' redeclared
21:12: '<init>' redeclared
22:12: '<init>' redeclared
40:18: 'erase' redeclared
40:18: 'erase' redeclared
41:18: 'erase' redeclared
41:18: 'erase' redeclared
41:18: 'erase' redeclared
42:20: 'erase' redeclared
45:35: 'insert' redeclared
45:35: 'insert' redeclared
46:23: 'insert' redeclared
"""
