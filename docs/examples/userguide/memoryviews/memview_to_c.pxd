cdef extern from "C_func_file.c":
    # C is include here so that it doesn't need to be compiled externally
    pass

cdef extern from "C_func_file.h":
    void multiply_by_10_in_C(double *, unsigned int)
