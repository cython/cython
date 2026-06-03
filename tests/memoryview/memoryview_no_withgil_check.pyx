# mode: compile

# cython: test_fail_if_c_code_has = __Pyx_ErrOccurredWithGIL

# cython-generated memoryview code shouldn't resort to
# __Pyx_ErrOccurredWithGIL for error checking (because it's inefficient
# inside a nogil block)

def assign(double[:] a, double[:] b):
    with nogil:
        a[:] = b[:]
