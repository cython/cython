import cython
from cython.cimports.libc.stdio import FILE, fopen
from cython.cimports.libc.stdlib import malloc, free
from cython.cimports.cpython.exc import PyErr_SetFromErrnoWithFilenameObject

def open_file():
    p: cython.pointer(FILE) = fopen("spam.txt", "r")
    if p is cython.NULL:
        PyErr_SetFromErrnoWithFilenameObject(OSError, "spam.txt")
    ...


def allocating_memory(number=10):
    my_array: cython.p_double = cython.cast(p_double, malloc(number * cython.sizeof(double)))
    if not my_array:  # same as 'is NULL' above
        raise MemoryError()
    ...
    free(my_array)
