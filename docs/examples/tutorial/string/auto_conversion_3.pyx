# cython: c_string_type=unicode, c_string_encoding=ascii

def func():
    ustring = u'abc'
    cdef char* s = ustring
    return s[0]    # returns u'a'
