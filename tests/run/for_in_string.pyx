cimport cython

bytes_abc = b'abc'
bytes_ABC = b'ABC'

unicode_abc = u'abc'
unicode_ABC = u'ABC'


def for_in_bytes(bytes s):
    """
    >>> for_in_bytes(bytes_abc)
    'X'
    >>> for_in_bytes(bytes_ABC)
    'C'
    """
    for c in s:
        # Py2/Py3
        if c == b'C' or c == c'C':
            return 'C'
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_char_in_bytes(bytes s):
    """
    >>> for_char_in_bytes(bytes_abc)
    'X'
    >>> for_char_in_bytes(bytes_ABC)
    'C'
    """
    cdef char c
    for c in s:
        if c == b'C':
            return 'C'
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_char_in_enumerate_bytes(bytes s):
    """
    >>> for_char_in_enumerate_bytes(bytes_abc)
    'X'
    >>> for_char_in_enumerate_bytes(bytes_ABC)
    2
    """
    cdef char c
    cdef Py_ssize_t i
    for i, c in enumerate(s):
        if c == b'C':
            return i
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_pyunicode_in_unicode(unicode s):
    """
    >>> for_pyunicode_in_unicode(unicode_abc)
    'X'
    >>> for_pyunicode_in_unicode(unicode_ABC)
    'C'
    """
    cdef Py_UNICODE c
    for c in s:
        if c == u'C':
            return 'C'
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_pyunicode_in_enumerate_unicode(unicode s):
    """
    >>> for_pyunicode_in_enumerate_unicode(unicode_abc)
    'X'
    >>> for_pyunicode_in_enumerate_unicode(unicode_ABC)
    2
    """
    cdef Py_UNICODE c
    cdef Py_ssize_t i
    for i, c in enumerate(s):
        if c == u'C':
            return i
    else:
        return 'X'
