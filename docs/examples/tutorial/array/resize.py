from cython.cimports.cpython import array
import array

a = cython.declare(array.array, array.array('i', [1, 2, 3]))
b = cython.declare(array.array, array.array('i', [4, 5, 6]))

# extend a with b, resize as needed
array.extend(a, b)
# resize a, leaving just original three elements
array.resize(a, len(a) - len(b))
