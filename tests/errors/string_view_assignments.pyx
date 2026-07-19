# mode: error
# coding: ASCII
# tag: cpp, cpp20

from libcpp.string_view cimport string_view

def get_obj():
    return b"123"

cdef bytes get_bytes():
    return b"123"

cdef string_view s1 = get_obj()  # bad, reference to temp
cdef string_view s2 = get_bytes()  # bad, reference to temp
cdef string_view s3 = u"123".encode()  # bad, reference to temp

_ERRORS = """
13:0: Storing unsafe C derivative of temporary Python reference
14:0: Storing unsafe C derivative of temporary Python reference
15:0: Storing unsafe C derivative of temporary Python reference
"""
