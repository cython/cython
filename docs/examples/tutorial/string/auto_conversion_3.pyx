# cython: c_string_type=unicode, c_string_encoding=UTF8

def func():
    ustring: str = 'abc'
    cdef const char* s = ustring
    return s[0]    # returns 'a' as a Unicode text string
