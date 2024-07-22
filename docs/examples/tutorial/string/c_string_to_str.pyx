from c_func cimport c_call_returning_a_c_string

cdef char* c_string = c_call_returning_a_c_string()
if c_string is NULL:
    ...  # handle error

cdef bytes py_string = c_string
