# distutils: language = c++

from libcpp.string cimport string

def get_bytes():
    py_bytes_object = b'hello world'
    cdef string s = py_bytes_object

    s.append('abc')
    py_bytes_object = s
    return py_bytes_object

