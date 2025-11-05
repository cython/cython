from cython.cimports.libc.stdlib import free
from cython.cimports.c_func import c_call_returning_a_c_string

py_string = cython.declare(bytes)
c_string = cython.declare(cython.p_char, c_call_returning_a_c_string())
try:
    py_string = c_string
finally:
    free(c_string)
