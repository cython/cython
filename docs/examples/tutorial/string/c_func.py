from cython.cimports.libc.stdlib import malloc
from cython.cimports.libc.string import strcpy, strlen

hello_world = cython.declare(cython.p_char, 'hello world')
n = cython.declare(cython.Py_ssize_t, strlen(hello_world))

@cython.cfunc
def c_call_returning_a_c_string() -> cython.p_char:
    c_string: cython.p_char = cython.cast(cython.p_char, malloc(
        (n + 1) * cython.sizeof(cython.char)))

    if not c_string:
        return cython.NULL  # malloc failed

    strcpy(c_string, hello_world)
    return c_string

@cython.cfunc
def get_a_c_string(c_string_ptr: cython.pp_char,
                   length: cython.p_Py_ssize_t) -> cython.int:
    c_string_ptr[0] = cython.cast(cython.p_char, malloc(
        (n + 1) * cython.sizeof(cython.char)))

    if not c_string_ptr[0]:
        return -1  # malloc failed

    strcpy(c_string_ptr[0], hello_world)
    length[0] = n
    return 0
