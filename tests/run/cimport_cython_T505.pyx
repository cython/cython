# ticket: t505

cimport cython

cdef extern from "Python.h":
    cdef cython.unicode PyUnicode_DecodeUTF8(char* s, Py_ssize_t size, char* errors)

def test_capi():
    """
    >>> print(test_capi())
    abc
    """
    return PyUnicode_DecodeUTF8("abc", 3, NULL)
