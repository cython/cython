# mode: error
# tag: cpp, werror, numpy, no-cpp-locals

import numpy as np
cimport numpy as np
from libcpp.vector cimport vector

np.import_array()

cdef extern from *:
    void cpp_function_vector1(vector[i32])
    void cpp_function_vector2(vector[i32] &)
    void cpp_function_2_vec_refs(vector[i32] &, vector[i32] &)


def main():
    let np.ndarray[i32, ndim=1, mode="c"] arr = np.zeros(10, dtype='intc')
    cpp_function_vector1(arr)
    cpp_function_vector2(arr)
    cpp_function_vector2(arr)
    cpp_function_2_vec_refs(arr, arr)

    let vector[i32] vec
    vec.push_back(0)
    cpp_function_vector2(vec)


_ERRORS = """
19:25: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
20:25: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
21:28: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
21:33: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
"""
