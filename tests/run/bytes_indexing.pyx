
cimport cython

cdef bytes b12345 = b'12345'

def index_literal(int i):
    """
    Python 3 returns integer values on indexing, Py2 returns byte
    string literals...

    >>> index_literal(0) in (ord('1'), '1')
    True
    >>> index_literal(-5) in (ord('1'), '1')
    True
    >>> index_literal(2) in (ord('3'), '3')
    True
    >>> index_literal(4) in (ord('5'), '5')
    True
    """
    return b"12345"[i]


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
def index_literal_char_cast(int i):
    """
    >>> index_literal_char_cast(0) == ord('1')
    True
    >>> index_literal_char_cast(-5) == ord('1')
    True
    >>> index_literal_char_cast(2) == ord('3')
    True
    >>> index_literal_char_cast(4) == ord('5')
    True
    >>> index_literal_char_cast(6)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return <char>(b"12345"[i])


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
def index_nonliteral_char_cast(int i):
    """
    >>> index_nonliteral_char_cast(0) == ord('1')
    True
    >>> index_nonliteral_char_cast(-5) == ord('1')
    True
    >>> index_nonliteral_char_cast(2) == ord('3')
    True
    >>> index_nonliteral_char_cast(4) == ord('5')
    True
    >>> index_nonliteral_char_cast(6)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return <char>(b12345[i])


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
def index_literal_uchar_cast(int i):
    """
    >>> index_literal_uchar_cast(0) == ord('1')
    True
    >>> index_literal_uchar_cast(-5) == ord('1')
    True
    >>> index_literal_uchar_cast(2) == ord('3')
    True
    >>> index_literal_uchar_cast(4) == ord('5')
    True
    >>> index_literal_uchar_cast(6)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return <unsigned char>(b"12345"[i])


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
def index_nonliteral_uchar_cast(int i):
    """
    >>> index_nonliteral_uchar_cast(0) == ord('1')
    True
    >>> index_nonliteral_uchar_cast(-5) == ord('1')
    True
    >>> index_nonliteral_uchar_cast(2) == ord('3')
    True
    >>> index_nonliteral_uchar_cast(4) == ord('5')
    True
    >>> index_nonliteral_uchar_cast(6)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return <unsigned char>(b12345[i])


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
def index_literal_char_coerce(int i):
    """
    >>> index_literal_char_coerce(0) == ord('1')
    True
    >>> index_literal_char_coerce(-5) == ord('1')
    True
    >>> index_literal_char_coerce(2) == ord('3')
    True
    >>> index_literal_char_coerce(4) == ord('5')
    True
    >>> index_literal_char_coerce(6)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    cdef char result = b"12345"[i]
    return result


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
def index_nonliteral_char_coerce(int i):
    """
    >>> index_nonliteral_char_coerce(0) == ord('1')
    True
    >>> index_nonliteral_char_coerce(-5) == ord('1')
    True
    >>> index_nonliteral_char_coerce(2) == ord('3')
    True
    >>> index_nonliteral_char_coerce(4) == ord('5')
    True
    >>> index_nonliteral_char_coerce(6)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    cdef char result = b12345[i]
    return result


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
@cython.boundscheck(False)
def index_literal_char_coerce_no_check(int i):
    """
    >>> index_literal_char_coerce_no_check(0) == ord('1')
    True
    >>> index_literal_char_coerce_no_check(-5) == ord('1')
    True
    >>> index_literal_char_coerce_no_check(2) == ord('3')
    True
    >>> index_literal_char_coerce_no_check(4) == ord('5')
    True
    """
    cdef char result = b"12345"[i]
    return result


@cython.test_assert_path_exists("//PythonCapiCallNode")
@cython.test_fail_if_path_exists("//IndexNode",
                                 "//CoerceFromPyTypeNode")
@cython.boundscheck(False)
def index_nonliteral_char_coerce_no_check(int i):
    """
    >>> index_nonliteral_char_coerce_no_check(0) == ord('1')
    True
    >>> index_nonliteral_char_coerce_no_check(-5) == ord('1')
    True
    >>> index_nonliteral_char_coerce_no_check(2) == ord('3')
    True
    >>> index_nonliteral_char_coerce_no_check(4) == ord('5')
    True
    """
    cdef char result = b12345[i]
    return result
