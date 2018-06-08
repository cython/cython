cimport cython

cdef char* s = b"abcdefg"
cdef const char* cs = b"abcdefg"
cdef unsigned char* us = b"abcdefg"
cdef const unsigned char* cus = b"abcdefg"
cdef bytes pystr =  b"abcdefg"


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char():
    """
    >>> lentest_char()
    7
    """
    return len(s)


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_const_char():
    """
    >>> lentest_const_char()
    7
    """
    return len(cs)


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c():
    """
    >>> lentest_char_c()
    7
    """
    cdef Py_ssize_t l = len(s)
    return l


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c_short():
    """
    >>> lentest_char_c_short()
    7
    """
    cdef short l = len(s)
    return l


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c_float():
    """
    >>> lentest_char_c_float()
    7.0
    """
    cdef float l = len(s)
    return l


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_uchar():
    """
    >>> lentest_uchar()
    7
    """
    return len(us)


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_const_uchar():
    """
    >>> lentest_const_uchar()
    7
    """
    return len(cus)


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_uchar_c():
    """
    >>> lentest_uchar_c()
    7
    """
    cdef Py_ssize_t l = len(us)
    return l


def lentest_py():
    """
    >>> lentest_py()
    7
    """
    return len(pystr)


def lentest_py_c():
    """
    >>> lentest_py_c()
    7
    """
    cdef Py_ssize_t l = len(pystr)
    return l
