# mode: compile
from libc.stdlib cimport malloc, free

cdef void f():
    cdef const int **allocated = <const int **>malloc(sizeof(int *))
    free(allocated)

f()
