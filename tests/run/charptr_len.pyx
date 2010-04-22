__doc__ = """
>>> lentest_char()
7
>>> lentest_char_c()
7
>>> lentest_char_c_short()
7
>>> lentest_char_c_float()
7.0

>>> lentest_uchar()
7
>>> lentest_uchar_c()
7

>>> lentest_py()
7
>>> lentest_py_c()
7
"""


cimport cython

cdef char* s = b"abcdefg"
cdef unsigned char* us = b"abcdefg"
cdef bytes pystr =  b"abcdefg"


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char():
    return len(s)

@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c():
    cdef Py_ssize_t l = len(s)
    return l

@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c_short():
    cdef short l = len(s)
    return l

@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c_float():
    cdef float l = len(s)
    return l


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_uchar():
    return len(us)

@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_uchar_c():
    cdef Py_ssize_t l = len(us)
    return l


def lentest_py():
    return len(pystr)

def lentest_py_c():
    cdef Py_ssize_t l = len(pystr)
    return l
