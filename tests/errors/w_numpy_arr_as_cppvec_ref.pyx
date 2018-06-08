# mode: error
# tag: cpp, werror, numpy

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
17:25: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
18:25: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
19:28: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
19:33: Cannot pass Python object as C++ data structure reference (vector[int] &), will pass by copy.
"""
