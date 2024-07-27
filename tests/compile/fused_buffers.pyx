# mode: compile

# cython: test_assert_c_code_has = __Pyx_ImportNumPyArrayTypeIfAvailable
# cython: test_assert_c_code_has = ndarray

# counterpart test to fused_no_numpy - buffer types are compared against Numpy
# dtypes as a quick test. fused_no_numpy tests that the mechanism isn't
# accidentally generated, while this just confirms that the same mechanism is
# still in use

ctypedef fused IntOrFloat:
    int
    float

def f(IntOrFloat[:] x):
    return x
