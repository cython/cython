from libc.stdlib cimport free
from c_func cimport c_call_returning_a_c_string

cdef bytes py_string
cdef char* c_string = c_call_returning_a_c_string()
try:
    py_string = c_string
finally:
    free(c_string)
