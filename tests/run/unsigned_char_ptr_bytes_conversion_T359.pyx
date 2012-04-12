# ticket: 359

cdef unsigned char* some_c_unstring = 'test toast taste'

def test_uchar_conversion():
    """
    >>> py_string1, py_string2, py_string3 = test_uchar_conversion()
    >>> print(py_string1.decode('iso8859-1'))
    test toast taste
    >>> print(py_string2.decode('iso8859-1'))
    test toast taste
    >>> print(py_string3.decode('iso8859-1'))
    test toast taste
    """

    cdef object py_string1 = some_c_unstring

    cdef unsigned char* c_unstring_from_py = py_string1
    cdef object py_string2 = c_unstring_from_py

    cdef char* c_string_from_py = py_string2
    cdef object py_string3 = c_string_from_py

    return py_string1, py_string2, py_string3
