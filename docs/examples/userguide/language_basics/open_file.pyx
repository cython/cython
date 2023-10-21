from libc.stdio cimport FILE, fopen
from libc.stdlib cimport malloc, free
from cpython.exc cimport PyErr_SetFromErrnoWithFilenameObject

def open_file():
    cdef FILE* p
    p = fopen("spam.txt", "r")
    if p is NULL:
        PyErr_SetFromErrnoWithFilenameObject(OSError, "spam.txt")
    ...


def allocating_memory(number=10):
    cdef f64 *my_array = <f64 *> malloc(number * sizeof(f64))
    if not my_array:  # same as 'is NULL' above
        raise MemoryError()
    ...
    free(my_array)
