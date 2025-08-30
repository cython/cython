from cython.cimports.cpython import array
import array
a = cython.declare(array.array, array.array('i', [1, 2, 3]))
ca = cython.declare(cython.int[:], a)

print(ca[0])
