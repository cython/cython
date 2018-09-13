# cython: c_string_type=unicode, c_string_encoding=utf8

cdef char* c_string = 'abcdefg'

# implicit decoding:
cdef object py_unicode_object = c_string

# explicit conversion to Python bytes:
py_bytes_object = <bytes>c_string
