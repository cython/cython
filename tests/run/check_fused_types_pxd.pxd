cimport cython

ctypedef cython.fused_type(int, float) unresolved_t
