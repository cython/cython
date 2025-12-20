import numpy as np
import cython

myarray: cython.int[:, ::1] = np.arange(20, dtype=np.intc).reshape((2, 10))

my_fused_type = cython.fused_type(cython.int[:, ::1], cython.float[:, ::1])



def func(array: my_fused_type):
    print("func called:", cython.typeof(array))

func["int[:, ::1]"](myarray)
