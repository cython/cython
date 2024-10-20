from cython.cimports.c_func import c_call_returning_a_c_string

some_c_string = cython.declare(cython.p_char, c_call_returning_a_c_string())
ustring = some_c_string.decode('UTF-8')
