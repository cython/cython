# distutils: language = c++

from cython.cimports.libcpp.string import string

def get_bytes():
    py_bytes_object = b'hello world'
    s: string = py_bytes_object

    s.append(b'abc')
    py_bytes_object = s
    return py_bytes_object
