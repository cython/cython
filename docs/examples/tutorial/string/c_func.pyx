from libc.stdlib cimport malloc
from libc.string cimport strcpy, strlen

cdef char* hello_world = 'hello world'
cdef Py_ssize_t n = strlen(hello_world)


cdef char* c_call_returning_a_c_string():
    cdef char* c_string = <char *> malloc((n + 1) * sizeof(char))
    if not c_string:
        raise MemoryError()
    strcpy(c_string, hello_world)
    return c_string


cdef void get_a_c_string(char** c_string_ptr, Py_ssize_t *length):
    c_string_ptr[0] = <char *> malloc((n + 1) * sizeof(char))
    if not c_string_ptr[0]:
        raise MemoryError()

    strcpy(c_string_ptr[0], hello_world)
    length[0] = n
