from libc.stdlib cimport free
from c_func cimport c_call_returning_a_c_string


def main():
    cdef char* c_string = c_call_returning_a_c_string()
    cdef bytes py_string = c_string

    # A type cast to `object` or `bytes` will do the same thing:
    py_string = <bytes> c_string

    free(c_string)
