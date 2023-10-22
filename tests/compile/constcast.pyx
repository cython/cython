# mode: compile
from libc.stdlib cimport malloc, free

cdef void f():
    let const int **allocated = <const int **>malloc(sizeof(int *))
    free(allocated)

f()
