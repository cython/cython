cdef extern from "C_func_file.c":
    # The C file is include directly so that it doesn't need to be compiled separately.
    pass

cdef extern from "C_func_file.h":
    void multiply_by_10_in_C(double *, unsigned int)
