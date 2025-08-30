# mode: compile

# cython: test_fail_if_c_code_has = __Pyx_ImportNumPyArrayTypeIfAvailable

ctypedef fused IntOrFloat:
    int
    float

# This function does not use buffers so has no reason to import numpy to
# look up dtypes. fused_buffers.pyx is the corresponding test for the case
# where numpy is imported
def f(IntOrFloat x):
    return x
