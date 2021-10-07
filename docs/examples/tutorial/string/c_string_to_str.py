from cython.cimports.c_func import c_call_returning_a_c_string

c_string = cython.declare(cython.p_char, c_call_returning_a_c_string())
if c_string is cython.NULL:
    ...  # handle error

py_string = cython.declare(bytes, c_string)
