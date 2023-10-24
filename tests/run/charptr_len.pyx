cimport cython

cdef char* s = b"abcdefg"
cdef const char* cs = b"abcdefg"
cdef u8* us = b"abcdefg"
cdef const u8* cus = b"abcdefg"
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
    let isize l = len(s)
    return l

@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c_short():
    """
    >>> lentest_char_c_short()
    7
    """
    let i16 l = len(s)
    return l

@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    )
def lentest_char_c_float():
    """
    >>> lentest_char_c_float()
    7.0
    """
    let f32 l = len(s)
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
    let isize l = len(us)
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
    let isize l = len(pystr)
    return l
