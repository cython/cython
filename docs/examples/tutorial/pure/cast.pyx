from libc.stddef cimport size_t 

ctypedef int* T

cdef size_t t 

t = 12345

t1 = <size_t><T>t

t2 = <size_t><T?>t
