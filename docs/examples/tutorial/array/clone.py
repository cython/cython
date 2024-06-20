from cython.cimports.cpython import array
import array

int_array_template = cython.declare(array.array, array.array('i', []))
cython.declare(newarray=array.array)

# create an array with 3 elements with same type as template
newarray = array.clone(int_array_template, 3, zero=False)
