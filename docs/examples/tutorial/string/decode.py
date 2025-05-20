from cython.cimports.c_func import get_a_c_string

c_string = cython.declare(cython.p_char, cython.NULL)
length = cython.declare(cython.Py_ssize_t, 0)

# get pointer and length from a C function
get_a_c_string(cython.address(c_string), cython.address(length))

ustring = c_string[:length].decode('UTF-8')
