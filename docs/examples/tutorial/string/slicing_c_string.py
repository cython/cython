from cython.cimports.libc.stdlib import free
from cython.cimports.c_func import get_a_c_string


def main():
    c_string: cython.p_char = cython.NULL
    length: cython.Py_ssize_t = 0

    # get pointer and length from a C function
    get_a_c_string(cython.address(c_string), cython.address(length))

    try:
        py_bytes_string = c_string[:length]  # Performs a copy of the data
    finally:
        free(c_string)
