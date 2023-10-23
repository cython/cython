from libc.stdlib cimport malloc
from libc.string cimport strcpy, strlen

cdef char* hello_world = 'hello world'
cdef usize n = strlen(hello_world)

fn char* c_call_returning_a_c_string():
    let char* c_string = <char *> malloc((n + 1) * sizeof(char))
    if not c_string:
        return NULL  # malloc failed

    strcpy(c_string, hello_world)
    return c_string

fn void get_a_c_string(char** c_string_ptr, isize *length):
    c_string_ptr[0] = <char *> malloc((n + 1) * sizeof(char))
    if not c_string_ptr[0]:
        return  # malloc failed

    strcpy(c_string_ptr[0], hello_world)
    length[0] = n
