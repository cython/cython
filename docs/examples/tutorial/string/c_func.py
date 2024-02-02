from cython.cimports.libc.stdlib import malloc
from cython.cimports.libc.string import strcpy, strlen

hello_world = cython.declare(cython.p_char, 'hello world')
n = cython.declare(cython.Py_ssize_t, strlen(hello_world))


# this function is defined as a cdef function in the .pxd file, no need for @cython.cfunc
def c_call_returning_a_c_string() -> cython.p_char:
    c_string: cython.p_char = cython.cast(cython.p_char, malloc(
        (n + 1) * cython.sizeof(cython.char)))

    if not c_string:
        return cython.NULL  # malloc failed

    strcpy(c_string, hello_world)
    return c_string


# this function is defined as a cdef function in the .pxd file, no need for @cython.cfunc
@cython.cfunc  # DELETE ME (GH#5970)
def get_a_c_string(c_string_ptr: cython.pp_char,
                   length: cython.pointer(cython.Py_ssize_t)) -> cython.void:
    c_string_ptr[0] = cython.cast(cython.p_char, malloc(
        (n + 1) * cython.sizeof(cython.char)))

    if not c_string_ptr[0]:
        return  # malloc failed

    strcpy(c_string_ptr[0], hello_world)
    length[0] = n
