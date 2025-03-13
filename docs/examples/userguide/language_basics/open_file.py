from cython.cimports.libc.stdio import FILE, fopen
from cython.cimports.libc.stdlib import malloc, free
from cython.cimports.cpython.exc import PyErr_SetFromErrnoWithFilenameObject

def open_file():
    p = fopen("spam.txt", "r")   # The type of "p" is "FILE*", as returned by fopen().

    if p is cython.NULL:
        PyErr_SetFromErrnoWithFilenameObject(OSError, "spam.txt")
    ...


def allocating_memory(number=10):
    # Note that the type of the variable "my_array" is automatically inferred from the assignment.
    my_array = cython.cast(p_double, malloc(number * cython.sizeof(double)))
    if not my_array:  # same as 'is NULL' above
        raise MemoryError()
    ...
    free(my_array)
