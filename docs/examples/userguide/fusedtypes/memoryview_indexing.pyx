import numpy as np
import cython

myarray: cython.int[:, ::1] = np.arange(20, dtype=np.intc).reshape((2, 10))

ctypedef fused my_fused_type:
    int[:, ::1]
    float[:, ::1]

def func(my_fused_type array):
    print("func called:", cython.typeof(array))

func["int[:, ::1]"](myarray)
