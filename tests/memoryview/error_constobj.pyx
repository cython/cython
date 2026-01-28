# mode: error

import numpy as np

# Cannot qualify plain object 'const'
cdef const object a  # <<< error

# Cannot assign to const memoryview
arr = np.array([object() for _ in range(10)])
cdef const object[:] arrview = arr
arrview[2] = object()  # <<< error


_ERRORS = u"""
6:5: Const/volatile base type cannot be a Python object
11:7: Assignment to const dereference
"""
