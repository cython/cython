from cpython cimport array
import array

cdef array.array int_array_template = array.array('i', [])
cdef array.array newarray

# create an array with 3 elements with same type as template
newarray = array.clone(int_array_template, 3, zero=False)
