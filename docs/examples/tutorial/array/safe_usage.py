import cython
from cython.cimports.cpython import array
import array
a = cython.declare(array.array)
ca = cython.declare(cython.int[:])
a = array.array('i', [1, 2, 3])
ca = a

print(ca[0])
