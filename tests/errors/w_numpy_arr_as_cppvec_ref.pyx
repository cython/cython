# mode: error
# tag: werror

import numpy as np
cimport numpy as np
from libcpp.vector cimport vector

cdef extern from *:
    void cpp_function_vector1(vector[int])
    void cpp_function_vector2(vector[int] &)
    void cpp_function_2_vec_refs(vector[int] &, vector[int] &)


def main():
    cdef np.ndarray[int, ndim=1, mode="c"] arr = np.zeros(10, dtype='intc')
    cpp_function_vector1(arr)
    cpp_function_vector2(arr)
    cpp_function_vector2(arr)
    cpp_function_2_vec_refs(arr, arr)

    cdef vector[int] vec
    vec.push_back(0)
    cpp_function_vector2(vec)


_ERRORS = """
17:28: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
18:28: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
19:31: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
19:36: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
31:15: '<init>' redeclared
31:15: '<init>' redeclared
32:15: '<init>' redeclared
32:15: '<init>' redeclared
32:15: '<init>' redeclared
33:15: '<init>' redeclared
33:15: '<init>' redeclared
33:15: '<init>' redeclared
34:15: '<init>' redeclared
44:19: 'assign' redeclared
44:19: 'assign' redeclared
45:35: 'assign' redeclared
55:22: 'erase' redeclared
55:22: 'erase' redeclared
56:22: 'erase' redeclared
58:23: 'insert' redeclared
58:23: 'insert' redeclared
59:19: 'insert' redeclared
59:19: 'insert' redeclared
59:19: 'insert' redeclared
60:19: 'insert' redeclared
69:19: 'resize' redeclared
69:19: 'resize' redeclared
70:19: 'resize' redeclared
"""
