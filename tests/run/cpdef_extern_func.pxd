# cython: c_string_type=str
# cython: c_string_encoding=ascii

extern from "math.h":
    cpdef double pxd_sqrt "sqrt"(double)
