# distutils: extra_compile_args=-std=c++0x
# tag: cpp

import cython

cimport libcpp

cimport libcpp.array

from libcpp.array  cimport *

cdef libcpp.array.array[int, 10]   a1 = array[int, 10]()

cdef array[int, 10].iterator ia1 = a1.begin()
cdef array[int, 10].iterator ia2 = a1.end()
cdef array[int, 10].reverse_iterator ria1 = a1.rbegin()
cdef array[int, 10].reverse_iterator ria2 = a1.rend()
