# ticket: 359

__doc__ = """
>>> print(py_string1.decode('iso8859-1'))
test toast taste
>>> print(py_string2.decode('iso8859-1'))
test toast taste
>>> print(py_string3.decode('iso8859-1'))
test toast taste
"""

cdef unsigned char* some_c_unstring = 'test toast taste'

py_string1 = some_c_unstring

cdef unsigned char* c_unstring_from_py = py_string1

py_string2 = c_unstring_from_py

cdef char* c_string_from_py = py_string2

py_string3 = c_string_from_py
