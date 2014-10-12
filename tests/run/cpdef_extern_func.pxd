# cython: c_string_type=str
# cython: c_string_encoding=ascii

cdef extern from "math.h":
    cpdef double pxd_sqrt "sqrt"(double)
